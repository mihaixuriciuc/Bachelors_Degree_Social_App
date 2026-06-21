"""
Targets check_duplicate_posts (TF-IDF cosine on title+content blobs).
Reworded promotional posts — not identical, but near-duplicate. Needs 3+
posts and 2+ similar pairs.

Run:
    python manage.py seed_duplicate_posts
    python manage.py seed_duplicate_posts --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, make_post, clear_by_tag

EXTRA_TAG = "duplicate_posts.seedbot.test"

POSTS = [
    ("Huge sale today", "Grab our amazing discounts before they are gone today"),
    ("Huge sale now", "Grab the amazing discounts before they're gone right now"),
    ("Big sale today", "Get our amazing discounts before they are gone today"),
    ("Massive sale", "Grab these amazing discounts before they are gone today"),
]


class Command(BaseCommand):
    help = "Seed a user with reworded near-duplicate posts (TF-IDF)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding duplicate-posts bot..."))

        bot = make_user(
            username="postdupe_real",
            bio="Local shop owner sharing offers.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )
        for title, content in POSTS:
            make_post(bot, title, content)

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'postdupe_real' has reworded duplicate posts → "
            "check_duplicate_posts."
        ))