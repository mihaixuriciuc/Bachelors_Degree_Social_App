"""
Targets check_duplicate_image: the same image FILENAME reused across 3+
posts. The check reads the stored filename (not file content), so a fake
path reused across posts triggers it — no real file needed.

Run:
    python manage.py seed_duplicate_image
    python manage.py seed_duplicate_image --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, make_post, clear_by_tag

EXTRA_TAG = "duplicate_image.seedbot.test"

# Same filename in every post's image path → reused-image signal.
SAME_IMAGE = "user_test/post_content/promo_banner.png"


class Command(BaseCommand):
    help = "Seed a user reusing the same image filename across posts."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding duplicate-image bot..."))

        bot = make_user(
            username="imagedupe_real",
            bio="Posting my favourite picture a lot.",
            with_pic=True,
            extra_tag=EXTRA_TAG,
        )

        # 4 posts, all with the SAME image filename (threshold is 3).
        # Distinct, non-duplicate text so the duplicate-POSTS check stays
        # quiet — isolating the image check.
        texts = [
            ("My day", "A good morning to start the week off well."),
            ("Thoughts", "Thinking about the weekend plans ahead."),
            ("Update", "Quick update on what I have been up to lately."),
            ("Evening", "Winding down after a long productive day."),
        ]
        for title, content in texts:
            make_post(bot, title, content, image=SAME_IMAGE)

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'imagedupe_real' reused one image across 4 posts → "
            "check_duplicate_image."
        ))