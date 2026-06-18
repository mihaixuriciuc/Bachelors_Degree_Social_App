from rest_framework.throttling import UserRateThrottle

from .services import EventLogger


class LoggingUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        self.request = request
        return super().allow_request(request, view)

    def throttle_failure(self):
        request = getattr(self, 'request', None)
        if request is not None:
            EventLogger.log_throttled(request, detail=f"scope: {self.scope}")
        return super().throttle_failure()