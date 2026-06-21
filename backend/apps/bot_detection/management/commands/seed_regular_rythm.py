"""
Targets check_regular_rhythm: 5+ actions spaced almost EXACTLY evenly
(low standard deviation of gaps) with a short average gap. Humans are
irregular; bots on a timer are mechanically even.

We backdate actions to be exactly 60s apart → near-zero stddev, well under
RHYTHM_STDDEV_THRESHOLD (2.0s) and under RHYTHM_MAX_AVG_GAP_SECONDS (120s).

Run:
    python manage.py seed_regular_rhythm
    python manage.py seed_regular_rhythm --clear
"""

from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand

from ._bot_helpers import make_user, make_post, clear_by_tag

EXTRA_TAG = "regular_rhythm.seedbot.test"


class Command(BaseCommand):
    help = "Seed a user posting at perfectly even intervals (mechanical rhythm)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding mechanical-rhythm bot..."))

        bot = make_user(
            username="metronome_real",
            bio="Posting regular updates.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # 8 posts, each EXACTLY 60 seconds apart → stddev ~0.
        # Distinct content so duplicate checks stay quiet.
        now = timezone.now()
        for i in range(8):
            make_post(
                bot,
                f"Scheduled update {i}",
                f"Automated-looking distinct content piece {i}.",
                created_at=now - timedelta(seconds=60 * i),
            )

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'metronome_real' posted 8x at exactly 60s intervals → "
            "check_regular_rhythm (near-zero timing variation)."
        ))