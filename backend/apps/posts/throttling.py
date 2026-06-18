from rest_framework.throttling import UserRateThrottle

from apps.bot_detection.services import EventLogger


class LoggingUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        # Stash the request so throttle_failure can access it later.
        # DRF doesn't pass the request into throttle_failure directly,
        # so we save a reference to it here first.
        self.request = request
        return super().allow_request(request, view)

    def throttle_failure(self):
        request = getattr(self, 'request', None)
        if request is not None:
            EventLogger.log_throttled(request, detail=f"scope: {self.scope}")
        return super().throttle_failure()


class PostCreationThrottle(LoggingUserRateThrottle):

    scope = 'post_create'


class CommentCreationThrottle(LoggingUserRateThrottle):
    scope = 'comment_create'


class LikeCreationThrottle(LoggingUserRateThrottle):
    scope = 'like_create'