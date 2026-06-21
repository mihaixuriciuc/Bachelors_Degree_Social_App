"""
Targets check_duplicate_post_burst: 3+ posts within POST_BURST_WINDOW_MINUTES
that are ALSO near-duplicates of each other. The conjunction (fast + similar)
is the signal — stronger than either alone.

Uses backdating so all posts fall inside the 10-minute window.

Run:
    python manage.py seed_duplicate_post_burst
    python manage.py seed_duplicate_post_burst --clear
"""

from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, make_post, clear_by_tag

EXTRA_TAG = "dup_post_burst.seedbot.test"

POSTS = [
    ("Flash deal", "Limited flash deal on now, grab yours before it ends"),
    ("Flash deal now", "Limited flash deal happening now, grab yours before it ends"),
    ("Flash deal today", "A limited flash deal on now, get yours before it ends"),
    ("Flash sale", "Limited flash deal on right now, grab yours before it ends"),
]


class Command(BaseCommand):
    help = "Seed a burst of near-duplicate posts in a short window."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding duplicate-post-burst bot..."))

        bot = make_user(
            username="burster_real",
            bio="Excited to share these offers!",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # All within the last few minutes → inside the burst window.
        now = timezone.now()
        for i, (title, content) in enumerate(POSTS):
            # Spread them 1 minute apart, all within ~4 min (< 10 min window).
            make_post(bot, title, content,
                      created_at=now - timedelta(minutes=i))

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'burster_real' posted 4 near-duplicate posts in minutes → "
            "check_duplicate_post_burst (and likely check_duplicate_posts too)."
        ))

