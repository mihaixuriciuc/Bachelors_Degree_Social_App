"""
Seeds test accounts to demonstrate the bot detection system.

Run with:
    python manage.py seed_bots

Each account is designed to trigger specific heuristics, plus two clean
"human" accounts that should NOT be flagged (to prove no false positives).

Run with --clear to delete previously seeded test accounts first:
    python manage.py seed_bots --clear

After seeding, go to the admin dashboard and click "Recompute Scores" to
see the accounts get scored and flagged.
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.user.models import User, Profile, Follow
from apps.posts.models import Post, Comment, Like
from apps.bot_detection.models import BotEvent


# A tag we put in the email so --clear knows which accounts are test data.
TEST_TAG = "seedbot.test"


class Command(BaseCommand):
    help = "Create test bot/human accounts to demonstrate detection."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete previously seeded test accounts before creating new ones.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self._clear()

        self.stdout.write(self.style.NOTICE("Seeding test accounts..."))

        # We need a "victim" post that bots can spam-comment on, and some
        # accounts for the follow-bot to follow. Create a clean human first.
        alice = self._make_user("alice_real", bio="Photographer and coffee lover.", with_pic=True)
        bob = self._make_user("bob_real", bio="Just here for the memes.", with_pic=True)

        # Give the humans some varied, normal activity.
        self._make_varied_comments(alice)
        self._make_varied_comments(bob)
        host_post = Post.objects.create(
            author=alice, title="My weekend trip", content="Had a great time hiking!"
        )

        # --- BOT 1: the obvious one (username pattern + blocklist + spam + repeat + no profile) ---
        cryptobot = self._make_user("cryptobot8472", bio=None, with_pic=False)
        for _ in range(5):
            Comment.objects.create(
                author=cryptobot, post=host_post,
                content="Check my profile for free crypto!!!",
            )

        # --- BOT 2: content spammer (blocklist + spam phrases + repeated) ---
        spammer = self._make_user("spammer_promo", bio=None, with_pic=False)
        for _ in range(4):
            Comment.objects.create(
                author=spammer, post=host_post,
                content="Click here to make money fast! DM me now.",
            )

        # --- BOT 3: auto-generated username (pattern + no profile) ---
        self._make_user("user99284756", bio=None, with_pic=False)

        # --- BOT 4: follow farm (blocklist + follow velocity) ---
        follow_bot = self._make_user("followfarm_f4f", bio=None, with_pic=False)
        # Create a bunch of targets and follow them all just now (high velocity).
        for i in range(25):
            target = self._make_user(f"target_{i}", bio="x", with_pic=False)
            Follow.objects.create(follower=follow_bot, following=target)

        # --- BOT 5: activity burst (many mixed actions in a short window) ---
        burst_bot = self._make_user("burst_bot", bio="hi", with_pic=False)
        # All created "now", so they fall inside the burst window.
        for i in range(8):
            Post.objects.create(author=burst_bot, title=f"post {i}", content="spam content")
        for i in range(10):
            Comment.objects.create(author=burst_bot, post=host_post, content=f"comment {i}")
        # Like a bunch of posts quickly.
        burst_targets = Post.objects.all()[:10]
        for p in burst_targets:
            Like.objects.get_or_create(author=burst_bot, post=p)

        # --- BOT 6: regular rhythm (evenly spaced actions) ---
        rhythm_bot = self._make_user("rhythm_bot", bio="tick tock", with_pic=False)
        # Create likes with timestamps exactly 60 seconds apart.
        # We can't set created_at on insert (auto_now_add), so we update after.
        base_time = timezone.now() - timedelta(hours=1)
        rhythm_targets = Post.objects.all()[:6]
        for i, p in enumerate(rhythm_targets):
            like, created = Like.objects.get_or_create(author=rhythm_bot, post=p)
            # Force an exact 60-second spacing.
            Like.objects.filter(pk=like.pk).update(
                created_at=base_time + timedelta(seconds=i * 60)
            )

        # Add a couple of throttle/failed-login events for some bots so the
        # event-based checks have data too.
        BotEvent.objects.create(
            user=cryptobot, ip_address="203.0.113.45",
            event_type=BotEvent.EventType.THROTTLED, detail="scope: comment_create",
        )
        BotEvent.objects.create(
            user=cryptobot, ip_address="203.0.113.45",
            event_type=BotEvent.EventType.THROTTLED, detail="scope: comment_create",
        )
        # Shared IP: put spammer on the SAME ip as cryptobot and a few targets.
        for u in [spammer, follow_bot]:
            BotEvent.objects.create(
                user=u, ip_address="203.0.113.45",
                event_type=BotEvent.EventType.THROTTLED, detail="scope: post_create",
            )

        self.stdout.write(self.style.SUCCESS("Done seeding."))
        self.stdout.write(
            "Now open the admin dashboard and click 'Recompute Scores' to see results."
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _make_user(self, username, bio=None, with_pic=False):
        """Create an active user + profile. Email carries the TEST_TAG."""
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@{TEST_TAG}",
                "is_active": True,
            },
        )
        if created:
            user.set_password("testpass123")
            user.save()

        # The post_save signal may have created the profile already.
        profile, _ = Profile.objects.get_or_create(user=user)
        if bio is not None:
            profile.bio = bio
        # We don't attach a real image file; "with_pic" is simulated by setting
        # a non-empty name so the completeness check sees a picture.
        # In a real test you'd upload an actual file; for scoring purposes the
        # check only looks at whether profile_pic is truthy.
        if with_pic:
            profile.profile_pic = "user_test/profile_picture/placeholder.png"
        profile.save()
        return user

    def _make_varied_comments(self, user):
        """Give a human account some normal, non-repeating comments."""
        # Need a post to comment on.
        post = Post.objects.create(
            author=user, title=f"{user.username}'s thoughts",
            content="Sharing something today.",
        )
        varied = [
            "Love this!",
            "Great point, thanks for sharing.",
            "I had a similar experience last week.",
            "Not sure I agree, but interesting.",
        ]
        for text in varied:
            Comment.objects.create(author=user, post=post, content=text)

    def _clear(self):
        """Delete all previously seeded test accounts (by email tag)."""
        qs = User.objects.filter(email__endswith=TEST_TAG)
        count = qs.count()
        qs.delete()  # cascades to their posts, comments, likes, follows, events
        self.stdout.write(self.style.WARNING(f"Cleared {count} test accounts."))