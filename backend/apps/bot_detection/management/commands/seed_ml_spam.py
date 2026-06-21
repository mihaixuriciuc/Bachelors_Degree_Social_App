"""
Targets the Naive Bayes checks (check_spam_comments / check_spam_bio) with
text the trained model recognizes CONFIDENTLY as spam.

Why a new command: the older seed_ml_spam used very subtly-worded comments
that the SMS-trained model scored below the 0.8 threshold, so the per-comment
spam_count never reached 2 and nothing fired. This version uses spam phrased
in the style the model was actually trained on (prizes, urgency, "claim",
"winner", "cash now") — which it flags with high confidence — while still
AVOIDING the hardcoded SpamPhrase entries, so it remains a CLASSIFIER-only
demo (no phrase-list overlap).

Each bot gets 4 such comments (threshold is 2), so even if one scores low,
the count still clears. Clean usernames + spammy bios; profile is complete
so only the ML checks fire.

Run:
    python manage.py seed_ml_classifier
    python manage.py seed_ml_classifier --clear
"""

from django.core.management.base import BaseCommand

from apps.posts.models import Post, Comment
from ._bot_helpers import make_user, clear_by_tag

EXTRA_TAG = "ml_classifier.seedbot.test"

# Spam in the SMS-corpus style the model knows well — high-confidence spam,
# but none of these are in the hardcoded SpamPhrase list (verify against
# yours). Each bot gets 4 so spam_count comfortably clears the threshold.
ML_BOTS = [
    {
        "username": "jenna_morris",
        "bio": "Congratulations! You have been selected to claim your free "
               "reward, text YES now to receive it.",
        "comments": [
            "URGENT: You have won a cash prize of 1000, call now to claim "
            "before it expires.",
            "Congratulations, your number was selected to receive a free "
            "reward, reply to claim now.",
            "You have been chosen to receive a special cash bonus, respond "
            "now to secure it.",
            "Final notice: claim your guaranteed prize today, text the code "
            "to the number below.",
        ],
    },
    {
        "username": "kevin_blake",
        "bio": "WINNER! Your account qualifies for an exclusive cash reward, "
               "claim before midnight tonight.",
        "comments": [
            "You have been awarded a bonus prize, call this number now to "
            "collect your winnings.",
            "Claim your free gift card now, you have been selected as today's "
            "lucky winner.",
            "Your mobile number won a prize draw, text CLAIM now to receive "
            "your reward.",
            "Act now to receive your guaranteed cash bonus before the offer "
            "expires tonight.",
        ],
    },
    {
        "username": "laura_finch",
        "bio": "You have a pending reward waiting. Reply CLAIM to receive your "
               "free prize today.",
        "comments": [
            "Congratulations you are our winner today, call now to claim your "
            "cash prize before it ends.",
            "Free entry confirmed: you have won, text the code now to collect "
            "your reward instantly.",
            "Your number has been selected for a guaranteed bonus, reply now "
            "to claim your winnings.",
            "Limited time: claim your free cash reward now, call the number "
            "to receive it today.",
        ],
    },
    {
        "username": "danny_reed",
        "bio": "Selected winner of this week's cash giveaway. Text now to "
               "claim your guaranteed reward.",
        "comments": [
            "URGENT reply needed: you have won a prize, call now to claim "
            "your reward before midnight.",
            "You are today's lucky winner, text YES now to receive your free "
            "cash bonus instantly.",
            "Your account won a special reward, reply CLAIM now to collect "
            "your winnings today.",
            "Congratulations, claim your guaranteed prize now before this "
            "final offer expires.",
        ],
    },
]


class Command(BaseCommand):
    help = "Seed bots with high-confidence classifier spam (Naive Bayes demo)."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            clear_by_tag(EXTRA_TAG, self.stdout, self.style)
            return

        self.stdout.write(self.style.NOTICE(
            "Seeding Naive Bayes classifier demo bots..."
        ))

        host_post = Post.objects.exclude(
            author__email__icontains="seedbot.test"
        ).first()
        if host_post is None:
            first = make_user(
                username=ML_BOTS[0]["username"],
                bio=ML_BOTS[0]["bio"],
                with_pic=True,
                extra_tag=EXTRA_TAG,
            )
            host_post = Post.objects.create(
                author=first, title="A normal post", content="Just sharing."
            )

        for data in ML_BOTS:
            user = make_user(
                username=data["username"],
                bio=data["bio"],
                with_pic=True,      # complete profile — isolate the ML checks
                extra_tag=EXTRA_TAG,
            )
            for text in data["comments"]:
                Comment.objects.get_or_create(
                    author=user, post=host_post, content=text
                )
            self.stdout.write(
                f"  Created '{data['username']}' "
                f"({len(data['comments'])} spam comments + spam bio)"
            )

        self.stdout.write(self.style.SUCCESS(
            "\nDone. Recompute → these flag on ML_SPAM_COMMENT / ML_SPAM_BIO.\n"
            "If they still don't fire, run the per-text probability check "
            "and lower SPAM_CLASSIFIER_THRESHOLD, or restart the server "
            "(stale cached model)."
        ))