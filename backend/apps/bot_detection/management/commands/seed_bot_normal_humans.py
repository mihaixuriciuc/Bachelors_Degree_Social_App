"""
Creates a batch of realistic human-like accounts for testing.
These should all score 0 / not be flagged — they're the control group
that proves the detection system doesn't produce false positives.

Run:
    python manage.py bot_normal_humans
    python manage.py bot_normal_humans --count 50
    python manage.py bot_normal_humans --clear
"""

import random

from django.core.management.base import BaseCommand

from apps.user.models import User, Profile
from apps.posts.models import Post, Comment

EXTRA_TAG = "normalhuman.seedbot.test"

FIRST_NAMES = [
    "alice", "bob", "elena", "mihai", "ana", "george", "ioana", "andrei",
    "maria", "stefan", "diana", "alex", "cristina", "vlad", "raluca",
    "florin", "carmen", "radu", "simona", "dan", "irina", "paul",
    "gabriela", "victor", "monica", "tudor", "laura", "bogdan", "alina", "marius",
]

LAST_NAMES = [
    "popescu", "ionescu", "stanescu", "dumitrescu", "georgescu", "constantin",
    "marin", "stoica", "radu", "matei", "barbu", "nistor", "florea", "vasile",
]

BIOS = [
    "Photographer and coffee lover.",
    "Software student. Always learning something new.",
    "Book reader. Amateur cook. Dog person.",
    "Traveller. Always planning the next trip.",
    "Just here for the memes and good conversations.",
    "Building things on the internet.",
    "Music, hiking, and too much coffee.",
    "Trying to read more books this year.",
    "Cat person. Plant parent. Occasional chef.",
    "Working on my thesis, send help.",
    "",  # some humans genuinely leave it blank
    "Lover of long walks and short naps.",
]

POST_TITLES_AND_CONTENT = [
    ("My weekend trip", "Finally made it to the mountains. Worth every step."),
    ("Morning routine", "Coffee first, then everything else."),
    ("Thoughts on clean code", "Readable code is a gift to your future self."),
    ("Recipe I tried", "Turned out way better than I expected."),
    ("Currently reading", "Three chapters in and already hooked."),
    ("Random thought", "Why does the week always go by faster than the weekend."),
    ("New setup", "Finally organized my desk, feels like a fresh start."),
    ("Today was good", "Nothing special happened, but it was a good day anyway."),
    ("Question for everyone", "What's a small thing that made you happy this week?"),
    ("Late night thoughts", "Can't sleep, so here's a post instead."),
]

COMMENT_POOL = [
    "Really enjoyed reading this!",
    "Great point, I had a similar experience.",
    "Not sure I agree, but interesting perspective.",
    "Thanks for sharing this.",
    "This made me smile, thank you.",
    "I felt this way too last month.",
    "Where was this taken? Looks amazing.",
    "Following for more like this.",
    "Honestly relatable.",
    "Saving this for later.",
    "Same energy, love it.",
    "Wow, never thought about it that way.",
]


class Command(BaseCommand):
    help = "Seed realistic human-like accounts (control group, should score 0)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=30,
            help='How many accounts to create (default: 30).',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete previously seeded normal-human accounts.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            qs = User.objects.filter(email__endswith=EXTRA_TAG)
            count = qs.count()
            qs.delete()
            self.stdout.write(self.style.WARNING(f"Cleared {count} accounts."))
            return

        count = options['count']
        self.stdout.write(self.style.NOTICE(f"Seeding {count} normal human accounts..."))

        created_users = []

        for i in range(count):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            # Mix of naming styles real people actually use.
            style = random.choice([
                f"{first}_{last}",
                f"{first}.{last}",
                f"{first}{last}",
                f"{first}_{last}{random.randint(1, 99)}",
            ])
            username = f"{style}_{i}"  # _i guarantees uniqueness across runs

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@{EXTRA_TAG}",
                    "is_active": True,
                    "first_name": first.capitalize(),
                    "last_name": last.capitalize(),
                },
            )
            if created:
                user.set_password("testpass123")
                user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.bio = random.choice(BIOS)
            # Most humans have a profile picture; some don't.
            if random.random() < 0.7:
                profile.profile_pic = "user_test/profile_picture/placeholder.png"
            profile.save()

            created_users.append(user)

        self.stdout.write(f"  Created {len(created_users)} accounts.")

        # Give each user 1-3 posts with varied, non-repeating content.
        for user in created_users:
            num_posts = random.randint(1, 3)
            chosen_posts = random.sample(POST_TITLES_AND_CONTENT, num_posts)
            for title, content in chosen_posts:
                Post.objects.get_or_create(
                    author=user,
                    title=title,
                    defaults={"content": content},
                )

        self.stdout.write("  Created posts for each account.")

        # Give each user a few varied comments on OTHER users' posts.
        all_posts = list(Post.objects.exclude(author__in=created_users))
        if not all_posts:
            all_posts = list(Post.objects.all())

        for user in created_users:
            if not all_posts:
                break
            num_comments = random.randint(2, 5)
            for _ in range(num_comments):
                target_post = random.choice(all_posts)
                comment_text = random.choice(COMMENT_POOL)
                Comment.objects.get_or_create(
                    author=user,
                    post=target_post,
                    content=comment_text,
                )

        self.stdout.write("  Created varied comments for each account.")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. Created {count} normal human accounts.\n"
            "After Recompute, all of these should score 0 — "
            "they're the control group proving no false positives."
        ))