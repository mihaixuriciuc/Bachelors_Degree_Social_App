"""
Targets check_follow_velocity: 20+ follows within
FOLLOW_VELOCITY_WINDOW_MINUTES (60 min). Backdated into the window.

NOTE: 20+ follows in 5 min would ALSO trip check_activity_burst. To isolate
follow-velocity, we spread the follows across ~50 minutes (over the 5-min
burst window) so ONLY the hourly follow check fires.

Run:
    python manage.py seed_follow_velocity
    python manage.py seed_follow_velocity --clear
"""

from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand

from apps.user.models import Follow
from ._bot_helpers import make_user, clear_by_tag, backdate

EXTRA_TAG = "follow_velocity.seedbot.test"


class Command(BaseCommand):
    help = "Seed a user following 20+ accounts within an hour."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding follow-velocity bot..."))

        bot = make_user(
            username="follower_real",
            bio="Connecting with lots of people.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # Create 25 targets and follow them all, spread across ~50 minutes
        # (so it stays within the 60-min window but OUTSIDE the 5-min burst
        # window — isolating follow-velocity from activity-burst).
        now = timezone.now()
        for i in range(25):
            target = make_user(
                username=f"fv_target_{i}",
                bio="A target.",
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
            f = Follow.objects.create(follower=bot, following=target)
            # Spread: 2 minutes apart → 25 follows over ~48 min.
            backdate(f, now - timedelta(minutes=2 * i))

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'follower_real' followed 25 accounts within the hour "
            "(spread out) → check_follow_velocity only."
        ))