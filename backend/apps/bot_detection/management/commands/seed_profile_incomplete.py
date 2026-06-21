"""
Targets check_profile_completeness: no picture AND no bio.

Usernames are clean and human-looking so ONLY the profile check fires —
isolating it.

Run:
    python manage.py seed_profile_incomplete
    python manage.py seed_profile_incomplete --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "profile_incomplete.seedbot.test"

USERNAMES = ["emptyone", "blankuser", "noinfohere", "quietaccount"]


class Command(BaseCommand):
    help = "Seed accounts with no bio and no picture (check_profile_completeness)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding incomplete-profile accounts..."))
        for name in USERNAMES:
            make_user(
                username=name,
                bio=None,            # no bio
                with_pic=False,      # no pic
                extra_tag=EXTRA_TAG,
            )
            self.stdout.write(f"  Created '{name}' (empty profile)")
        self.stdout.write(self.style.SUCCESS(
            "\nDone. Recompute → these flag on incomplete profile."
        ))