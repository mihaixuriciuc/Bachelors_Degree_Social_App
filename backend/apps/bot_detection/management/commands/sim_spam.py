import time
from django.core.management.base import BaseCommand
from ._http_client import APIClient, SocialAppBot, random_string, force_activate, get_target_post_id


class Command(BaseCommand):
    help = "Simulates comment spam bots (Exact matches vs Varied spam phrases)."

    def handle(self, *args, **options):
        BASE_URL = "http://localhost:8000/api/v1"
        target_post_id = get_target_post_id()

        self.stdout.write(self.style.NOTICE("--- Starting Spam Simulations ---"))

        # Scenario A: Exact Same Message Spam
        client_a = APIClient(BASE_URL, ip_address="10.0.0.101")
        bot_a = SocialAppBot(client_a)
        user_a = f"spam_exact_{random_string()}"

        bot_a.sign_up(user_a, "SecurePass123!")
        force_activate(user_a)
        bot_a.sign_in(user_a, "SecurePass123!")

        self.stdout.write(f"[{user_a}] Posting exact same message multiple times...")
        spam_msg = "Click link in bio for free stuff!"
        for i in range(4):
            res = bot_a.comment_on_post(target_post_id, spam_msg)
            self.stdout.write(f"  Comment {i + 1}: {res.status_code}")
            time.sleep(21)  # Wait slightly to avoid standard throttle, hitting the repeat threshold instead

        # Scenario B: Varied Blocklist Phrase Spam
        client_b = APIClient(BASE_URL, ip_address="10.0.0.102")
        bot_b = SocialAppBot(client_b)
        user_b = f"spam_varied_{random_string()}"

        bot_b.sign_up(user_b, "SecurePass123!")
        force_activate(user_b)
        bot_b.sign_in(user_b, "SecurePass123!")

        self.stdout.write(f"\n[{user_b}] Posting different spam phrases from blocklist...")
        phrases = ["buy crypto now", "follow for follow", "click here to win", "hot singles in your area"]
        for i, phrase in enumerate(phrases):
            res = bot_b.comment_on_post(target_post_id, phrase)
            self.stdout.write(f"  Phrase '{phrase}': {res.status_code}")
            time.sleep(21)

        self.stdout.write(self.style.SUCCESS("Spam simulation complete."))