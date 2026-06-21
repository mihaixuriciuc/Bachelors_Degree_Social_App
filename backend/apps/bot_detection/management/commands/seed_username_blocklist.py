"""
Targets check_username_blocklist (exact substring + fuzzy Levenshtein).

The exact ones contain a blocklisted term outright; the fuzzy ones are a
small edit-distance away from a blocklisted term (obfuscated spelling),
proving the Levenshtein fuzzy match catches near-misses.

NOTE: this depends on your BlocklistTerm table being populated
(populate_patterns). The fuzzy examples assume common terms like 'crypto',
'casino', 'promo' exist — adjust to match your actual blocklist.

Run:
    python manage.py seed_username_blocklist
    python manage.py seed_username_blocklist --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "uname_blocklist.seedbot.test"

# Clean letters only (no digits) so check_username_pattern stays quiet —
# isolating the blocklist check.
EXACT = [
    "cryptoking",      # contains 'crypto'
    "casinoroyale",    # contains 'casino'
    "bestpromodeals",  # contains 'promo'
]
FUZZY = [
    "cryptoo",         # 1 edit from 'crypto'
    "casin0royale",    # 'casino' with o->0 obfuscation (edit distance)
    "promol",          # close to 'promo'
]


class Command(BaseCommand):
    help = "Seed blocklist-matching usernames (exact + fuzzy Levenshtein)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE("Seeding blocklist usernames..."))
        for name in EXACT + FUZZY:
            make_user(
                username=name,
                bio="Sharing deals and updates daily.",
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
            self.stdout.write(f"  Created '{name}'")
        self.stdout.write(self.style.SUCCESS(
            "\nDone. Exact names flag on substring match; fuzzy names flag on "
            "Levenshtein distance. Verify against your populated blocklist."
        ))