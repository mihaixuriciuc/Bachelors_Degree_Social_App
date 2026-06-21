"""
Hand-written labeled examples for the spam classifier, in the style of
social-media comments and bios. These are mixed with a larger public
dataset (SMS Spam Collection) at training time — the public data gives
volume, these give domain flavor (comment/bio spam differs from SMS spam).

Each entry is (text, label) where label is 'spam' or 'ham' ('ham' is the
conventional term for 'not spam').
"""

SPAM_EXAMPLES = [
    "Check my profile for free crypto giveaway!",
    "Follow me and I follow back instantly!!",
    "Click the link in my bio to make money fast",
    "DM me to earn $500 a day from home",
    "Free followers here just visit my page",
    "Investment opportunity guaranteed 200% returns",
    "Buy now limited offer act fast",
    "Hot singles in your area click here",
    "Win a free iPhone click the link below",
    "Join my telegram for crypto signals",
    "Get rich quick with this one trick",
    "Follow for follow lets grow together f4f",
    "Best forex signals dm for details",
    "Double your bitcoin in 24 hours",
    "Subscribe to my channel and earn rewards",
    "Visit my website for exclusive deals",
    "Make passive income while you sleep",
    "Claim your prize now you have been selected",
    "Cheap followers and likes available dm me",
    "Crypto airdrop free tokens limited time",
    "Promote your business contact me now",
    "Earn money online no experience needed",
    "Adult content check my page link in bio",
    "Giveaway winner click to claim your reward",
    "Trading bot makes you rich automatically",
    "Free gift card just complete this survey",
    "Whatsapp me for amazing business deals",
    "Lose weight fast with this miracle product",
    "Get verified badge for cheap dm now",
    "Massive discount today only buy buy buy",
]

HAM_EXAMPLES = [
    "Really enjoyed this post, thanks for sharing!",
    "I had a similar experience last weekend.",
    "Not sure I agree but it's an interesting point.",
    "Photographer and coffee lover from Cluj.",
    "Where was this photo taken? Looks beautiful.",
    "Software student interested in AI and music.",
    "This made my day, thank you so much.",
    "Great write-up, learned something new today.",
    "Honestly relatable, been there myself.",
    "Just here for the memes and good vibes.",
    "Love hiking and reading on weekends.",
    "Congrats on the new job, well deserved!",
    "I disagree with point two but the rest is solid.",
    "Anyone else reading this book right now?",
    "Trying to cook more at home these days.",
    "Beautiful shot, what camera did you use?",
    "Thanks for the recommendation, will check it out.",
    "Had a great time at the concert last night.",
    "Working on my thesis, wish me luck.",
    "This recipe looks delicious, saving it.",
    "Travelling through Europe this summer.",
    "Good morning everyone, hope you have a nice day.",
    "I think the second option makes more sense.",
    "Cat person, plant parent, occasional chef.",
    "That's a really thoughtful perspective.",
    "Been following your work for a while, great stuff.",
    "Can you share more details about this?",
    "Loved the ending, did not see it coming.",
    "Just finished a 10k run, feeling great.",
    "Music, books, and too much coffee.",
]