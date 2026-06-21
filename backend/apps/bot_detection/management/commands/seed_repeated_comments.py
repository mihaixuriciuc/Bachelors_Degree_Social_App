"""
Targets check_repeated_comments: the SAME comment text posted 3+ times.

Distinct from the TF-IDF near-duplicate check — this is exact repetition.
Clean username + complete profile so only this check fires.

Run:
    python manage.py seed_repeated_comments
    python manage.py seed_repeated_comments --clear
"""

from django.core.management.base import BaseCommand
from apps.posts.models import Post
from ._bot_helpers import make_user, make_comment, clear_by_tag

EXTRA_TAG = "repeated_comments.seedbot.test"


class Command(BaseCommand):
    help = "Seed a user posting the exact same comment many times."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding repeated-comment bot..."))

        bot = make_user(
            username="repeater_real",
            bio="Big fan of this community.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # Need a post to comment on. Use any existing one, else make one.
        host_post = Post.objects.exclude(
            author__email__icontains="seedbot.test"
        ).first()
        if host_post is None:
            host_post = Post.objects.create(
                author=bot, title="A post", content="Some content here."
            )

        # Same exact text 5 times (threshold is 3).
        text = "Love this, keep up the great work!"
        for _ in range(5):
            make_comment(bot, host_post, text)

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'repeater_real' posted the same comment 5x → "
            "check_repeated_comments."
        ))