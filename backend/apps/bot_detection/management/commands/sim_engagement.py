from django.core.management.base import BaseCommand
from apps.user.models import User
from ._http_client import APIClient, SocialAppBot, random_string, force_activate


class Command(BaseCommand):
    help = "Simulates mass following and mass liking bots."

    def handle(self, *args, **options):
        BASE_URL = "http://localhost:8000/api/v1"

        self.stdout.write(self.style.NOTICE("--- Starting Engagement Simulations ---"))

        client = APIClient(BASE_URL, ip_address="172.16.0.44")
        bot = SocialAppBot(client)
        user = f"follow_farmer_{random_string()}"

        bot.sign_up(user, "SecurePass123!")
        force_activate(user)
        bot.sign_in(user, "SecurePass123!")

        # Grab up to 25 random targets from the database to follow
        targets = list(User.objects.exclude(username=user).values_list('username', flat=True)[:25])

        if not targets:
            self.stdout.write(self.style.ERROR("Not enough users in the DB to follow. Seed some first!"))
            return

        self.stdout.write(f"[{user}] Mass-following {len(targets)} users...")
        for i, target in enumerate(targets):
            res = bot.follow_user(target)
            if res.status_code == 429:
                self.stdout.write(self.style.WARNING(f"  Follow {i + 1} ({target}): 429 THROTTLED"))
            else:
                self.stdout.write(f"  Follow {i + 1} ({target}): {res.status_code}")

        self.stdout.write(self.style.SUCCESS("Engagement simulation complete."))