"""
this is the constants script, where i have thresholds, points for the account score and bot keywords
"""
# --- Naive Bayes spam classifier ---
# How confident the classifier must be before we treat text as spam.
# 0.8 means "80%+ probability of spam" — higher than a coin-flip 0.5,
# to keep false positives low.
SPAM_CLASSIFIER_THRESHOLD = 0.8

# How many of a user's comments must be classified spam before the user
# is flagged. Requiring 2+ avoids flagging someone for a single comment
# the model might have misjudged.
SPAM_COMMENT_COUNT_THRESHOLD = 2

POST_SIMILARITY_THRESHOLD = 0.80
POST_SIMILAR_PAIR_THRESHOLD = 2      # how many near-duplicate pairs to flag
POST_SIMILARITY_MIN_POSTS = 3        # need at least this many posts to compare

DUPLICATE_IMAGE_THRESHOLD = 3


POST_BURST_WINDOW_MINUTES = 10       # the time window
POST_BURST_MIN_POSTS = 3             # min posts in window to consider
POST_BURST_SIMILARITY_THRESHOLD = 0.80   # how similar they must be


ACTIVITY_BURST_THRESHOLD = 30       #how many activities in total can someone do in activiti_burst_window before its flagged a bot
ACTIVITY_BURST_WINDOW_MINUTES = 5  #used to determine the window where some
RHYTHM_MIN_ACTIONS = 5
NEAR_DUPLICATE_SIMILARITY_THRESHOLD = 0.75
NEAR_DUPLICATE_PAIR_THRESHOLD = 2
NEAR_DUPLICATE_MIN_COMMENTS = 3


RHYTHM_STDDEV_THRESHOLD = 2.0

RHYTHM_MAX_AVG_GAP_SECONDS = 120

RHYTHM_WINDOW_HOURS = 24

RISK_TIER_SUSPICIOUS = 30
RISK_TIER_LIKELY_BOT = 55


FLAG_THRESHOLD = RISK_TIER_LIKELY_BOT


POINTS = {
    'username_pattern': 15,
    'username_blocklist': 20,
    'shared_ip': 20,
    'throttle_event': 10,
    'failed_login': 5,
    'repeated_comment': 25,
    'spam_phrase': 15,
    'follow_velocity': 15,
    'incomplete_profile': 10,
    'activity_burst': 20,         #if someone makes a lot of action in a time window
    'regular_rhythm': 20,        # if the comments/likes etc get posted at the same time interval
    'username_cluster': 20,
    'fuzzy_blocklist': 20,
    'fuzzy_cluster': 15,
    'near_duplicate_comments': 20,
    'duplicate_posts': 20,
    'duplicate_image': 15,
    'duplicate_post_burst': 25,   # highest — burst + duplication is strong signal
    'bot_network': 25,   # strong signal — dense mutual-follow farms are rarely innocent
    'spam_comments_ml': 20,
    'spam_bio_ml': 15,

}


THROTTLE_EVENT_CAP = 30
FAILED_LOGIN_CAP = 20


USERNAME_DIGIT_RATIO = 0.4


USERNAME_TRAILING_DIGITS = 4

SHARED_IP_THRESHOLD = 3


REPEATED_COMMENT_THRESHOLD = 3


FOLLOW_VELOCITY_THRESHOLD = 20
FOLLOW_VELOCITY_WINDOW_MINUTES = 60


USERNAME_CLUSTER_THRESHOLD = 3
CLUSTER_FUZZY_DISTANCE = 3
CLUSTER_MIN_STEM_LENGTH = 4


BOT_NETWORK_MIN_CLUSTER_SIZE = 5

# Minimum density (0.0-1.0): what fraction of all possible mutual-follow
# connections in the cluster actually exist. 0.7 means 70%+ of everyone
# in the cluster mutually follows everyone else — far denser than any
# natural friend group, a hallmark of a coordinated farm.
BOT_NETWORK_MIN_DENSITY = 0.7