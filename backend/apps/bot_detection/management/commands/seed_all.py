"""
Runs every bot-detection seed command in one go, creating a full population
that exercises every check in the engine — including the four complex
algorithms (Levenshtein, TF-IDF/cosine, connected components, Naive Bayes).

After running this, open the dashboard and Recompute. You should see each
seeded account flagged by its specific target check, while the normal-human
control group stays clean (proving no false positives).

Run:
    python manage.py seed_all
    python manage.py seed_all --clear      # tear everything down
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

# Order matters slightly: create the human/control population and real posts
# FIRST, so that seeds needing "a post to comment on" or "real users to
# camouflage-follow" have something to reference.
SEED_COMMANDS = [
    # Control group + real content first.
    "seed_bot_normal_humans",

    # --- Username + profile checks (Batch A) ---
    "seed_username_pattern",
    "seed_username_blocklist",       # Levenshtein (fuzzy blocklist)
    "seed_username_cluster",         # Levenshtein (fuzzy cluster)
    "seed_profile_incomplete",

    # --- Content checks (Batch B) ---
    "seed_repeated_comments",
    "seed_near_duplicate_comments",  # TF-IDF / cosine
    "seed_spam_phrases",
    "seed_duplicate_posts",          # TF-IDF / cosine
    "seed_duplicate_image",
    "seed_duplicate_post_burst",     # TF-IDF / cosine

    # --- Timing / behavior checks (Batch C) ---
    "seed_activity_burst",
    "seed_regular_rhythm",
    "seed_follow_velocity",

    # --- Event-based checks (Batch D) ---
    "seed_shared_ip",
    "seed_throttle_events",
    "seed_failed_logins",

    # --- Complex algorithms with existing seeds ---
    "seed_bot_follow_network",       # connected components
    "seed_ml_spam",                  # Naive Bayes
]


class Command(BaseCommand):
    help = "Run (or clear) every bot-detection seed command at once."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all seeded accounts from every seed command.',
        )

    def handle(self, *args, **options):
        clear = options['clear']
        action = "Clearing" if clear else "Seeding"

        self.stdout.write(self.style.NOTICE(
            f"=== {action} ALL bot-detection seed data ===\n"
        ))

        for command in SEED_COMMANDS:
            self.stdout.write(self.style.HTTP_INFO(f"\n>>> {command}"))
            try:
                if clear:
                    call_command(command, '--clear')
                else:
                    call_command(command)
            except Exception as e:
                # Don't let one failing seed stop the rest — report and move on.
                self.stdout.write(self.style.ERROR(
                    f"  !! {command} failed: {e}"
                ))

        if clear:
            self.stdout.write(self.style.SUCCESS(
                "\n=== All seed data cleared. ==="
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                "\n=== All seed data created. ===\n"
                "Next: open the dashboard and click Recompute.\n"
                "Expect: every bot archetype flagged by its target check; "
                "the normal-human control group stays clean."
            ))