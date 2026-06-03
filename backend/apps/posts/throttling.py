from rest_framework.throttling import UserRateThrottle


class PostCreationThrottle(UserRateThrottle):
    """
    Limits how many posts a single user can create per day.
    The actual number (e.g. '20/day') is set in settings.py under the
    'post_create' key.  Changing the rate doesn't require touching any code.
    """
    scope = 'post_create'


class CommentCreationThrottle(UserRateThrottle):
    """
    Limits how many comments a single user can post per hour.
    """
    scope = 'comment_create'


class LikeCreationThrottle(UserRateThrottle):
    """
    Limits how many likes a single user can create per hour.
    A high limit (300/hour) because likes are cheap actions, but you still
    want a ceiling to prevent scripted abuse.
    """
    scope = 'like_create'
