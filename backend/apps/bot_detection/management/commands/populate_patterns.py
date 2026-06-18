"""
One-time command to migrate the hardcoded USERNAME_BLOCKLIST and SPAM_PHRASES
constants into the database models.

Run once after the migration:
    python manage.py populate_patterns

Safe to run multiple times — uses get_or_create so it won't create duplicates.
"""

from django.core.management.base import BaseCommand

from apps.bot_detection.models import BlocklistTerm, SpamPhrase


# These are the original hardcoded values from constants.py.
# Once they're in the DB, you can manage them through the admin
# and these lists become irrelevant.
BLOCKLIST_TERMS = [
    # Crypto / financial scam
    'bot', 'crypto', 'bitcoin', 'btc', 'eth', 'nft', 'defi', 'token',
    'forex', 'trading', 'investor', 'profit', 'signal', 'pump',
    'airdrop', 'wallet', 'binance', 'coinbase',

    # Engagement bait / follow farms
    'spam', 'follow4follow', 'f4f', 'l4l', 'like4like', 'followback',
    'followme', 'gain', 'promo', 'giveaway', 'official_',

    # Adult / scam
    'xxx', 'onlyfans', 'nsfw', 'hot_girl', 'sexy', 'dating',

    # Generic bot signatures
    'free_', 'click', 'subscribe', 'viral', 'trending', 'cashapp',
    'paypal_', 'venmo_', 'account_', 'user_bot', 'auto_',

    # Auto-generated name patterns
    'tempuser', 'testbot', 'newuser_', 'account', 'unnamed',
]
SPAM_PHRASES = [
    # Engagement / follow bait
    'follow me', 'follow for follow', 'follow back', 'f4f', 'l4l',
    'like for like', 'check my profile', 'visit my profile',
    'follow my account', 'i follow back', 'follow everyone back',
    'gain followers', 'get followers fast',

    # Crypto / financial scam
    'crypto', 'bitcoin', 'investment opportunity', 'invest now',
    'free money', 'make money', 'earn money online', 'passive income',
    'financial freedom', 'trading signals', 'forex signals',
    'double your money', '100% profit', 'guaranteed returns',
    'dm me for profits', 'limited offer', 'exclusive deal',
    'risk free investment', 'get rich quick',

    # Link / redirect spam
    'click here', 'click the link', 'link in bio', 'link in profile',
    'check the link', 'visit my link', 'http://', 'https://', 'www.',
    'bit.ly', 't.me', 'join our channel',

    # Messaging platform redirects
    'dm me', 'message me', 'text me', 'contact me on',
    'telegram', 'whatsapp', 'instagram dm', 'snapchat me',
    'add me on', 'find me on',

    # Adult / dating spam
    'dating site', 'meet singles', 'hot singles', 'onlyfans',
    'check my photos', 'see my pics', 'adult content',
    'hookup', 'meet me tonight',

    # Giveaway / prize scam
    'you have been selected', 'congratulations you won',
    'claim your prize', 'free iphone', 'free gift card',
    'winner selected', 'enter to win', 'giveaway',

    # Generic bot comment filler
    'nice post', 'great content', 'amazing post keep it up',
    'buy now', 'shop now', 'order now', 'visit our store',
    'subscribe to my channel', 'check out my page',
]

class Command(BaseCommand):
    help = "Populate BlocklistTerm and SpamPhrase tables from the original constants."

    def handle(self, *args, **options):
        created_terms = 0
        for term in BLOCKLIST_TERMS:
            _, created = BlocklistTerm.objects.get_or_create(term=term)
            if created:
                created_terms += 1

        created_phrases = 0
        for phrase in SPAM_PHRASES:
            _, created = SpamPhrase.objects.get_or_create(phrase=phrase)
            if created:
                created_phrases += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_terms} blocklist terms "
            f"and {created_phrases} spam phrases."
        ))