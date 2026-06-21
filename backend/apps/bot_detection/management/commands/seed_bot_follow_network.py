"""
Creates a dense mutual-follow cluster — a group of bot accounts that all
follow each other, simulating a bot farm inflating follower counts.

This is the test data for check_bot_network (connected-components
detection). After seeding, recompute and all cluster members should be
flagged as a bot network.

Also creates a few "camouflage" follows (cluster bots following some real
users) so the cluster isn't perfectly isolated — proving the density
check still catches it even with some outside edges.

Run:
    python manage.py bot_follow_network
    python manage.py bot_follow_network --size 10
    python manage.py bot_follow_network --clear
"""

import random

from django.core.management.base import BaseCommand

from apps.user.models import User, Follow
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "follownet.seedbot.test"


class Command(BaseCommand):
    help = "Seed a dense mutual-follow bot cluster (for connected-components)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--size',
            type=int,
            default=8,
            help='Number of accounts in the cluster (default: 8).',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete previously seeded follow-network accounts.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        size = options['size']
        self.stdout.write(self.style.NOTICE(
            f"Seeding a dense mutual-follow cluster of {size} accounts..."
        ))

        # 1. Create the cluster accounts.
        cluster_users = []
        for i in range(size):
            user = make_user(
                username=f"netbot_{i}",
                bio="Crypto enthusiast | DM for collabs",
                with_pic=False,
                extra_tag=EXTRA_TAG,
            )
            cluster_users.append(user)

        # 2. Make EVERY account follow EVERY other account in the cluster.
        # This creates a fully-connected mutual-follow graph — density ~1.0,
        # the clearest possible bot-network signal.
        follow_count = 0
        for follower in cluster_users:
            for following in cluster_users:
                if follower.id == following.id:
                    continue  # don't follow yourself
                _, created = Follow.objects.get_or_create(
                    follower=follower,
                    following=following,
                )
                if created:
                    follow_count += 1

        self.stdout.write(
            f"  Created {size} accounts with {follow_count} mutual follows "
            f"(fully-connected cluster)."
        )

        # 3. Camouflage: have a few cluster bots also follow some real users,
        # so the cluster has edges leaving it. The density check should STILL
        # catch it, because the INTERNAL density stays high regardless of a
        # few outside follows.
        real_users = list(
            User.objects.filter(is_staff=False)
            .exclude(id__in=[u.id for u in cluster_users])
            .exclude(email__icontains="seedbot.test")[:5]
        )

        camouflage_count = 0
        if real_users:
            for bot in random.sample(cluster_users, min(3, len(cluster_users))):
                target = random.choice(real_users)
                _, created = Follow.objects.get_or_create(
                    follower=bot,
                    following=target,
                )
                if created:
                    camouflage_count += 1
            self.stdout.write(
                f"  Added {camouflage_count} camouflage follows "
                f"(cluster bots following real users)."
            )
        else:
            self.stdout.write(
                "  No real users found for camouflage follows (skipped)."
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created a dense cluster of {size} accounts.\n"
            "Recompute, and all cluster members should be flagged as a "
            "bot network."
        ))