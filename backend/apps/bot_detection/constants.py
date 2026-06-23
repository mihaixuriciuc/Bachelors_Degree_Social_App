"""
this is the constants script, where i have thresholds, points for the account score and bot keywords
"""
#check_username_pattern constants
USERNAME_DIGIT_RATIO = 0.4
USERNAME_TRAILING_DIGITS = 4

#check_shared_ip
SHARED_IP_THRESHOLD = 3

#limits how many points can be added to thorttle events
THROTTLE_EVENT_CAP = 30

#limits how many points can be added to failed login events
FAILED_LOGIN_CAP = 20

# repeatet comment after how many same comments gets flagged
REPEATED_COMMENT_THRESHOLD = 3

#between 60 minutes how many follows
FOLLOW_VELOCITY_WINDOW_MINUTES = 60

#after how many follows should be flagged
FOLLOW_VELOCITY_THRESHOLD = 20

#how many names should be the same after removing digits before flagging
USERNAME_CLUSTER_THRESHOLD = 3

#how short a stem word can be to be compared
CLUSTER_MIN_STEM_LENGTH = 4

#how many different actions should be applied to one word, min
CLUSTER_FUZZY_DISTANCE = 3

#the percentage two phrases must obtain to be flagged
NEAR_DUPLICATE_SIMILARITY_THRESHOLD = 0.75

#minimum of combinations needed
NEAR_DUPLICATE_PAIR_THRESHOLD = 2

#minimum of comments
NEAR_DUPLICATE_MIN_COMMENTS = 3

# need at least this many posts to compare
POST_SIMILARITY_MIN_POSTS = 3

# how many near-duplicate pairs to flag
POST_SIMILAR_PAIR_THRESHOLD = 2


POST_SIMILARITY_THRESHOLD = 0.80


DUPLICATE_IMAGE_THRESHOLD = 3


POST_BURST_WINDOW_MINUTES = 10       # the time window
POST_BURST_MIN_POSTS = 3             # min posts in window to consider
POST_BURST_SIMILARITY_THRESHOLD = 0.80   # how similar they must be


#
BOT_NETWORK_MIN_CLUSTER_SIZE = 5

BOT_NETWORK_MIN_DENSITY = 0.7

SPAM_CLASSIFIER_THRESHOLD = 0.8

SPAM_COMMENT_COUNT_THRESHOLD = 2



ACTIVITY_BURST_THRESHOLD = 30       #how many activities in total can someone do in activiti_burst_window before its flagged a bot
ACTIVITY_BURST_WINDOW_MINUTES = 5  #used to determine the window where some
RHYTHM_MIN_ACTIONS = 5


RHYTHM_STDDEV_THRESHOLD = 2.0

RHYTHM_MAX_AVG_GAP_SECONDS = 120

RHYTHM_WINDOW_HOURS = 24

RISK_TIER_SUSPICIOUS = 30
RISK_TIER_LIKELY_BOT = 55


FLAG_THRESHOLD = RISK_TIER_LIKELY_BOT


POINTS = {
    'username_pattern': 15,  #points per numbered username
    'username_blocklist': 20, #points if its on blocklist
    'shared_ip': 20,  # points if the ip is shared
    'throttle_event': 10,  #points per throttle action
    'failed_login': 5, # points per failed login
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

