"""
Seeds the BlocklistTerm and SpamPhrase tables with a starter set of known
bad usernames substrings and spam phrases. These tables back
check_username_blocklist and check_spam_phrases — without running this,
both checks have nothing to match against and will silently never fire.

Safe to re-run: uses get_or_create, so running this multiple times won't
create duplicates (term/phrase are unique fields).

Run:
    python manage.py populate_patterns
    python manage.py populate_patterns --clear   # remove all entries first
"""

from django.core.management.base import BaseCommand

from apps.bot_detection.models import BlocklistTerm, SpamPhrase

BLOCKLIST_TERMS = [
    # Crypto / financial scam
    "crypto", "bitcoin", "forex", "investment", "trading", "binaryoptions",
    "wealth", "richquick", "passiveincome", "earnmoney", "cashapp",
    # Engagement manipulation
    "followback", "f4f", "followforfollow", "likeforlike", "growmyaccount",
    "freefollowers", "freelikes", "boostfollowers",
    # Adult / dating spam
    "onlyfans", "hotsingles", "datingnow", "adultcontent", "nsfwlink",
    # Generic scam / promo
    "giveaway", "freegift", "claimnow", "winnerselected", "casino",
    "promo", "discountcode", "limitedoffer", "clearancesale",
    # Phishing / redirect style
    "verifyaccount", "clickhere", "linkinbio", "specialoffer", "bonuscash",
    # Bot-farm-style generic words
    "botaccount", "fakefollowers", "autofollow", "spambot",
]

SPAM_PHRASES = [
    # Crypto / financial
    "free crypto", "double your bitcoin", "guaranteed returns",
    "investment opportunity", "earn money online", "passive income",
    "make money fast", "get rich quick", "trading signals",
    "forex signals", "crypto airdrop",
    # Engagement bait
    "follow for follow", "like for like", "f4f", "follow back instantly",
    "cheap followers", "free followers", "grow your account",
    # Prizes / urgency
    "click here to win", "you have been selected", "claim your prize",
    "limited time offer", "act now", "winner selected", "free gift card",
    "congratulations you won", "claim now",
    # Adult / dating
    "hot singles in your area", "check my onlyfans", "adult content",
    "dm me for more",
    # Generic promo / scam
    "buy now limited offer", "huge discount today only",
    "visit my page for deals", "exclusive deal just for you",
    "verify your account now", "click the link in my bio",
    # Redirect / phishing style
    "click here to claim", "confirm your details", "urgent action required",
]


class Command(BaseCommand):
    help = "Seed BlocklistTerm and SpamPhrase tables with starter patterns."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing entries before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            term_count = BlocklistTerm.objects.count()
            phrase_count = SpamPhrase.objects.count()
            BlocklistTerm.objects.all().delete()
            SpamPhrase.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"Cleared {term_count} blocklist terms and "
                f"{phrase_count} spam phrases."
            ))

        self.stdout.write(self.style.NOTICE("Populating BlocklistTerm..."))
        term_created = 0
        for term in BLOCKLIST_TERMS:
            obj, created = BlocklistTerm.objects.get_or_create(term=term)
            if created:
                term_created += 1

        self.stdout.write(self.style.NOTICE("Populating SpamPhrase..."))
        phrase_created = 0
        for phrase in SPAM_PHRASES:
            obj, created = SpamPhrase.objects.get_or_create(phrase=phrase)
            if created:
                phrase_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Added {term_created} new blocklist terms "
            f"({len(BLOCKLIST_TERMS) - term_created} already existed) and "
            f"{phrase_created} new spam phrases "
            f"({len(SPAM_PHRASES) - phrase_created} already existed)."
        ))