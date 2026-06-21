"""
Targets check_activity_burst: 30+ total actions (posts + comments + likes +
follows) within ACTIVITY_BURST_WINDOW_MINUTES (5 min). All actions are
backdated into one tight window.

We use mixed action types and DISTINCT content so the duplicate/repeat
checks stay quiet — isolating the volume signal.

Run:
    python manage.py seed_activity_burst
    python manage.py seed_activity_burst --clear
"""

from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand

from apps.posts.models import Post, Like
from apps.user.models import Follow
from ._bot_helpers import (
    make_user, make_post, make_comment, clear_by_tag, backdate,
)

EXTRA_TAG = "activity_burst.seedbot.test"


class Command(BaseCommand):
    help = "Seed a user with 30+ actions in a 5-minute window."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding activity-burst bot..."))

        bot = make_user(
            username="bursty_real",
            bio="Very active community member.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # A few target users + posts to like/follow/comment on.
        targets = []
        for i in range(5):
            t = make_user(
                username=f"burst_target_{i}",
                bio="A target account.",
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
            targets.append(t)
        target_posts = [
            make_post(t, f"Post by target {i}", "Some unique content here.")
            for i, t in enumerate(targets)
        ]

        now = timezone.now()
        # Put every action ~10 seconds apart, all within ~4 minutes.
        def t(seconds):
            return now - timedelta(seconds=seconds)

        action_count = 0
        clock = 0

        # 10 distinct posts
        for i in range(10):
            make_post(bot, f"Burst post {i}",
                      f"Distinct content number {i} for the burst test.",
                      created_at=t(clock))
            clock += 8
            action_count += 1

        # 10 distinct comments
        for i in range(10):
            make_comment(bot, target_posts[i % len(target_posts)],
                         f"Distinct comment number {i} here.",
                         created_at=t(clock))
            clock += 8
            action_count += 1

        # 6 likes
        for i in range(6):
            like = Like.objects.create(
                author=bot, post=target_posts[i % len(target_posts)]
            )
            backdate(like, t(clock))
            clock += 8
            action_count += 1

        # 6 follows
        for i in range(min(5, len(targets))):
            f = Follow.objects.create(follower=bot, following=targets[i])
            backdate(f, t(clock))
            clock += 8
            action_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. 'bursty_real' has {action_count} actions in ~4 min → "
            "check_activity_burst."
        ))