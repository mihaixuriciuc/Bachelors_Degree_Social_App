"""
Shared helpers for the bot seed commands.

The underscore prefix tells Django this is NOT a management command — it's
a helper module the actual commands import from. Without the prefix Django
would try to treat it as a runnable command.
"""

from apps.user.models import User, Profile
SEED_TAG = "seedbot.test"


from apps.posts.models import Post, Comment
from apps.bot_detection.models import BotEvent


def backdate(queryset_or_obj, when):
    """
    Force created_at to a specific time. Needed because created_at uses
    auto_now_add=True, which ignores any value passed at creation — the
    only way to set it is an UPDATE after the row exists. Time-based checks
    (activity burst, rhythm, follow velocity, post burst) depend on this.
    """
    pk = queryset_or_obj.pk
    type(queryset_or_obj).objects.filter(pk=pk).update(created_at=when)


def make_post(user, title, content, image=None, created_at=None):
    """Create a post, optionally backdated and with an image filename."""
    post = Post.objects.create(author=user, title=title, content=content)
    if image is not None:
        # Store a fake image path; the duplicate-image check reads the
        # filename, the file doesn't need to physically exist for scoring.
        Post.objects.filter(pk=post.pk).update(image=image)
    if created_at is not None:
        backdate(post, created_at)
    return post


def make_comment(user, post, content, created_at=None):
    comment = Comment.objects.create(author=user, post=post, content=content)
    if created_at is not None:
        backdate(comment, created_at)
    return comment


def make_event(user, event_type, detail="", ip_address=None, created_at=None):
    """Write a BotEvent row directly (for IP/throttle/failed-login seeds)."""
    event = BotEvent.objects.create(
        user=user,
        event_type=event_type,
        detail=detail,
        ip_address=ip_address,
    )
    if created_at is not None:
        backdate(event, created_at)
    return event

def make_user(username, bio=None, with_pic=False, extra_tag=""):
    """
    Create an active user plus their profile. The email carries a tag so
    the account can be identified and deleted later by a --clear command.

    extra_tag lets a specific command tag its own accounts more narrowly
    (e.g. "follownet.seedbot.test") so you can clear just one archetype
    without touching the others. If not given, falls back to SEED_TAG.
    """
    email_tag = extra_tag if extra_tag else SEED_TAG

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@{email_tag}",
            "is_active": True,
        },
    )
    if created:
        user.set_password("testpass123")
        user.save()

    # The profile may already exist if a post_save signal creates one
    # automatically; get_or_create handles both cases.
    profile, _ = Profile.objects.get_or_create(user=user)

    if bio is not None:
        profile.bio = bio

    if with_pic:
        # Simulate having a picture without uploading a real file — the
        # profile-completeness check only looks at whether the field is
        # truthy, so a placeholder path is enough for testing.
        profile.profile_pic = "user_test/profile_picture/placeholder.png"

    profile.save()
    return user


def clear_by_tag(tag, stdout, style):
    """
    Delete all users whose email ends with the given tag.

    Deleting the users cascades to their posts, comments, likes, follows,
    and bot events (all have on_delete=CASCADE foreign keys to User), so
    this fully removes the seeded data in one step.
    """
    qs = User.objects.filter(email__endswith=tag)
    count = qs.count()
    qs.delete()
    stdout.write(style.WARNING(f"Cleared {count} accounts with tag '{tag}'."))