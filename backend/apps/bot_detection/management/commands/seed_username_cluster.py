"""
Targets check_username_cluster (shared digit-stripped stem) AND
check_fuzzy_username_cluster (Levenshtein-close names). Threshold is 3+.

- EXACT cluster: many accounts share one stem after stripping trailing
  digits ('target_0', 'target_1', ... all stem to 'target').
- FUZZY cluster: names that are edit-distance-close to each other but don't
  share an exact stem ('farmbot', 'farmb0t', 'farmb0t', 'farnbot').

These accounts WILL also trip check_username_pattern (they contain digits) —
that overlap is inherent to clustered bot names and is noted, not a bug.

Run:
    python manage.py seed_username_cluster
    python manage.py seed_username_cluster --count 6
    python manage.py seed_username_cluster --clear
"""

from django.core.management.base import BaseCommand
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "uname_cluster.seedbot.test"

FUZZY_NAMES = ["farmbot", "farmb0t", "farnbot", "farmbol", "tarmbot"]


class Command(BaseCommand):
    help = "Seed username clusters (exact-stem + fuzzy Levenshtein)."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=5,
                            help='Exact-stem cluster size (default 5).')
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        count = options['count']
        self.stdout.write(self.style.NOTICE("Seeding username clusters..."))

        # Exact-stem cluster: target_0 .. target_N all stem to 'target'.
        for i in range(count):
            make_user(
                username=f"target_{i}",
                bio="Account number " + str(i),
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
        self.stdout.write(f"  Created exact-stem cluster of {count} ('target_*').")

        # Fuzzy cluster: Levenshtein-close but distinct stems.
        for name in FUZZY_NAMES:
            make_user(
                username=name,
                bio="Just here to browse.",
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
        self.stdout.write(f"  Created fuzzy cluster of {len(FUZZY_NAMES)} ('farmbot'-like).")

        self.stdout.write(self.style.SUCCESS(
            "\nDone. 'target_*' flag on exact-stem cluster; 'farmbot'-like flag "
            "on fuzzy cluster. (They also trip username_pattern — expected.)"
        ))