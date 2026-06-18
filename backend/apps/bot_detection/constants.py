"""
this is the constants script, where i have thresholds, points for the account score and bot keywords
"""

ACTIVITY_BURST_THRESHOLD = 30       #how many activities in total can someone do in activiti_burst_window before its flagged a bot
ACTIVITY_BURST_WINDOW_MINUTES = 5  #used to determine the window where some
RHYTHM_MIN_ACTIONS = 5

RHYTHM_STDDEV_THRESHOLD = 2.0

RHYTHM_MAX_AVG_GAP_SECONDS = 120

RHYTHM_WINDOW_HOURS = 24


FLAG_THRESHOLD = 60


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
}


THROTTLE_EVENT_CAP = 30
FAILED_LOGIN_CAP = 20


USERNAME_DIGIT_RATIO = 0.4


USERNAME_TRAILING_DIGITS = 4

SHARED_IP_THRESHOLD = 3


REPEATED_COMMENT_THRESHOLD = 3


FOLLOW_VELOCITY_THRESHOLD = 20
FOLLOW_VELOCITY_WINDOW_MINUTES = 60


USERNAME_CLUSTER_THRESHOLD = 10
BLOCKLIST_FUZZY_DISTANCE = 2
CLUSTER_FUZZY_DISTANCE = 3
CLUSTER_MIN_STEM_LENGTH = 4


