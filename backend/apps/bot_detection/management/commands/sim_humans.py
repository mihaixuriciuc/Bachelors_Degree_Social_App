import time
import random
from django.core.management.base import BaseCommand
from ._http_client import APIClient, SocialAppBot, random_string, force_activate


class Command(BaseCommand):
    help = "Simulates real human behavior (The Control Group) to ensure no false positives."

    def handle(self, *args, **options):
        BASE_URL = "http://localhost:8000/api/v1"

        self.stdout.write(self.style.NOTICE("--- Starting Human Control Group Simulation ---"))

        # --- PERSONA 1: Alice ---
        client_alice = APIClient(BASE_URL, ip_address="82.76.1.15")  # Standard residential IP
        bot_alice = SocialAppBot(client_alice)
        user_alice = f"alice_real_{random_string(3)}"

        bot_alice.sign_up(user_alice, "HumanPass123!")
        force_activate(user_alice)
        bot_alice.sign_in(user_alice, "HumanPass123!")
        self.stdout.write(f"[{user_alice}] Logged in. Reading feed...")

        time.sleep(3)  # Simulating time spent thinking/typing

        res_alice = bot_alice.create_post(
            title="Morning Coffee",
            content="Finally checking out that new cafe in Cluj. The espresso is amazing!"
        )
        if res_alice.status_code in (200, 201):
            post_alice_id = res_alice.json().get("id")
            self.stdout.write(self.style.SUCCESS(f"  -> Created post (ID: {post_alice_id})"))
        else:
            self.stdout.write(self.style.ERROR("  -> Failed to create post."))
            return

        # --- PERSONA 2: Bob ---
        time.sleep(2)  # Time passes before Bob logs on
        client_bob = APIClient(BASE_URL, ip_address="86.120.4.99")
        bot_bob = SocialAppBot(client_bob)
        user_bob = f"bob_dev_{random_string(3)}"

        bot_bob.sign_up(user_bob, "HumanPass123!")
        force_activate(user_bob)
        bot_bob.sign_in(user_bob, "HumanPass123!")
        self.stdout.write(f"\n[{user_bob}] Logged in. Scrolling...")

        time.sleep(4)

        # Bob creates his own post
        res_bob = bot_bob.create_post(
            title="Thesis Update",
            content="Almost done with the backend architecture. Time for a break."
        )
        post_bob_id = res_bob.json().get("id") if res_bob.status_code in (200, 201) else None
        self.stdout.write(self.style.SUCCESS(f"  -> Created post (ID: {post_bob_id})"))

        time.sleep(3)  # Bob reads Alice's post

        # Bob comments on Alice's post
        bot_bob.comment_on_post(post_alice_id, "Looks great! Where is that cafe?")
        self.stdout.write(self.style.SUCCESS(f"  -> Commented on {user_alice}'s post."))

        # --- PERSONA 3: Charlie ---
        time.sleep(2)
        client_charlie = APIClient(BASE_URL, ip_address="193.226.5.10")
        bot_charlie = SocialAppBot(client_charlie)
        user_charlie = f"charlie_photo_{random_string(3)}"

        bot_charlie.sign_up(user_charlie, "HumanPass123!")
        force_activate(user_charlie)
        bot_charlie.sign_in(user_charlie, "HumanPass123!")
        self.stdout.write(f"\n[{user_charlie}] Logged in. Exploring...")

        time.sleep(5)  # Charlie takes longer to type

        # Charlie creates his post
        bot_charlie.create_post(
            title="Weekend plans",
            content="Going hiking in the Apuseni mountains this weekend. Any tips?"
        )
        self.stdout.write(self.style.SUCCESS(f"  -> Created a post."))

        time.sleep(2)

        # Charlie likes Alice's post and comments on Bob's post
        bot_charlie.like_post(post_alice_id)
        self.stdout.write(self.style.SUCCESS(f"  -> Liked {user_alice}'s post."))

        time.sleep(3)

        if post_bob_id:
            bot_charlie.comment_on_post(post_bob_id, "Good luck with the thesis man! You got this.")
            self.stdout.write(self.style.SUCCESS(f"  -> Commented on {user_bob}'s post."))

        self.stdout.write(self.style.SUCCESS(
            "\nHuman control group simulation complete. Check your dashboard - these users should score 0."))