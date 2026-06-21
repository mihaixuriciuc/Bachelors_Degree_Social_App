"""
Targets check_near_duplicate_comments (TF-IDF + cosine). Comments are
REWORDED variants of the same message — NOT byte-identical, so the exact
repeated-comment check misses them, but cosine similarity catches the
near-duplicate pattern. Needs 2+ similar pairs, 3+ comments minimum.

This is the demo that justifies TF-IDF over exact matching.

Run:
    python manage.py seed_near_duplicate_comments
    python manage.py seed_near_duplicate_comments --clear
"""

from django.core.management.base import BaseCommand
from apps.posts.models import Post
from ._bot_helpers import make_user, make_comment, clear_by_tag

EXTRA_TAG = "near_dup_comments.seedbot.test"

# Same meaning, slightly reworded each time → high cosine similarity,
# zero exact duplicates.
COMMENTS = [
    "Check out my page for amazing deals you can't miss today",
    "Check out my profile for amazing deals you don't want to miss today",
    "Visit my page for the amazing deals you can't miss right now",
    "Have a look at my page for amazing deals you shouldn't miss today",
]


class Command(BaseCommand):
    help = "Seed reworded near-duplicate comments (TF-IDF cosine)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding near-duplicate-comment bot..."))

        bot = make_user(
            username="reworder_real",
            bio="Sharing the best finds with everyone.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        host_post = Post.objects.exclude(
            author__email__icontains="seedbot.test"
        ).first()
        if host_post is None:
            host_post = Post.objects.create(
                author=bot, title="A post", content="Some content here."
            )

        for text in COMMENTS:
            make_comment(bot, host_post, text)

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'reworder_real' posted reworded duplicates → "
            "check_near_duplicate_comments (TF-IDF). No exact repeats."
        ))