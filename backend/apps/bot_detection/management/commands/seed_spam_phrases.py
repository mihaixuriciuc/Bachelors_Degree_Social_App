"""
Targets check_spam_phrases: a comment or bio containing a known spam phrase
from the SpamPhrase table.

NOTE: depends on populate_patterns having seeded the SpamPhrase table.
The phrases below assume common entries exist ('click here', 'free money').
Verify against your actual table and adjust.

Run:
    python manage.py seed_spam_phrases
    python manage.py seed_spam_phrases --clear
"""

from django.core.management.base import BaseCommand
from apps.posts.models import Post
from ._bot_helpers import make_user, make_comment, clear_by_tag

EXTRA_TAG = "spam_phrases.seedbot.test"


class Command(BaseCommand):
    help = "Seed accounts whose comment/bio contains a known spam phrase."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding spam-phrase accounts..."))

        # One flags via comment, one via bio — both paths of the check.
        comment_bot = make_user(
            username="phrasecomment_real",
            bio="Normal looking bio here.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )
        bio_bot = make_user(
            username="phrasebio_real",
            bio="Click here to win free money now!",   # phrase in bio
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        host_post = Post.objects.exclude(
            author__email__icontains="seedbot.test"
        ).first()
        if host_post is None:
            host_post = Post.objects.create(
                author=comment_bot, title="A post", content="Content."
            )

        make_comment(comment_bot, host_post,
                     "Click here to claim your free money now!")

        self.stdout.write(self.style.SUCCESS(
            "\nDone. One flags via comment phrase, one via bio phrase. "
            "Verify the phrases exist in your SpamPhrase table."
        ))