from django.core.management.base import BaseCommand
from ._http_client import APIClient, SocialAppBot, random_string, force_activate, get_target_post_id


class Command(BaseCommand):
    help = "Simulates bots triggering API rate limits / throttles (Comments, Posts, and Logins)."

    def handle(self, *args, **options):
        BASE_URL = "http://localhost:8000/api/v1"
        target_post_id = get_target_post_id()

        self.stdout.write(self.style.NOTICE("--- Starting Throttle Simulations ---"))

        client = APIClient(BASE_URL, ip_address="192.168.1.99")
        bot = SocialAppBot(client)
        user = f"throttle_bot_{random_string()}"

        bot.sign_up(user, "SecurePass123!")
        force_activate(user)
        bot.sign_in(user, "SecurePass123!")

        # 1. Comment Throttle
        self.stdout.write(f"[{user}] Firing rapid-fire comments (No delays)...")
        for i in range(6):
            res = bot.comment_on_post(target_post_id, f"Rapid fire comment {i}")
            if res.status_code == 429:
                self.stdout.write(self.style.WARNING(f"  Comment {i + 1}: 429 THROTTLED"))
            else:
                self.stdout.write(f"  Comment {i + 1}: {res.status_code}")

        # 2. Post Throttle (NEW)
        self.stdout.write(f"\n[{user}] Firing rapid-fire posts (No delays)...")
        for i in range(6):
            res = bot.create_post(
                title=f"Spam Post {i}",
                content="Trying to break the post creation rate limit!"
            )
            if res.status_code == 429:
                self.stdout.write(self.style.WARNING(f"  Post {i + 1}: 429 THROTTLED"))
            else:
                self.stdout.write(f"  Post {i + 1}: {res.status_code}")

        # 3. Failed Login Throttle / Cap
        self.stdout.write(f"\n[{user}] Attempting mass login failures...")
        for i in range(5):
            res = bot.sign_in("admin", f"bad_password_{i}")
            self.stdout.write(f"  Login attempt {i + 1}: {res.status_code}")

        self.stdout.write(self.style.SUCCESS("\nThrottle simulation complete."))
