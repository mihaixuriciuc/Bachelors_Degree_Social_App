"""
Targets check_username_pattern: usernames that are digit-heavy (>=40% digits)
or end in 4+ digits look auto-generated.

Each account gets a clean bio + pic so ONLY the username check fires
(profile-completeness stays quiet). Isolated demo.

Run:
    python manage.py seed_username_pattern
    python manage.py seed_username_pattern --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "uname_pattern.seedbot.test"

USERNAMES = [
    "user82910",       # mostly digits
    "x9k2j8401",       # digit-heavy + random
    "john88472",       # trailing 5 digits
    "bot00001",        # trailing digits
    "a1b2c3d4e5",      # 50% digits
]


class Command(BaseCommand):
    help = "Seed digit-heavy usernames (check_username_pattern)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding digit-heavy usernames..."))
        for name in USERNAMES:
            make_user(
                username=name,
                bio="Just an ordinary account sharing thoughts.",
                with_pic=True,           # keep profile complete — isolate the check
                extra_tag=EXTRA_TAG,
            )
            self.stdout.write(f"  Created '{name}'")
        self.stdout.write(self.style.SUCCESS(
            "\nDone. Recompute → these should flag on username pattern only."
        ))