"""
Shared helpers for all bot seed commands.
Not a management command itself (underscore prefix keeps Django from
treating it as one).
"""

from apps.user.models import User
from apps.posts.models import Post, Comment, Like
from apps.user.models import Follow
from apps.bot_detection.models import BotEvent

# Tag used in every seeded account's email so --clear can find them all.
SEED_TAG = "seedbot.test"


def make_user(username, bio=None, with_pic=False, extra_tag=""):
    """
    Create an active user + profile. Email carries the SEED_TAG so the
    account can be found and deleted by any command's --clear flag.

    extra_tag lets individual commands tag their own accounts more
    specifically (e.g. "cluster.seedbot.test") so you can clear just
    one archetype's accounts if needed.
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

    from apps.user.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)

    if bio is not None:
        profile.bio = bio
    if with_pic:
        # Simulate having a picture without uploading a real file.
        # The completeness check only looks at whether the field is truthy.
        profile.profile_pic = "user_test/profile_picture/placeholder.png"

    profile.save()
    return user


def clear_by_tag(tag, stdout, style):
    """Delete all users whose email ends with the given tag."""
    qs = User.objects.filter(email__endswith=tag)
    count = qs.count()
    qs.delete()  # cascades to posts, comments, likes, follows, events
    stdout.write(style.WARNING(f"Cleared {count} accounts with tag '{tag}'."))