from .models import BotEvent
from .helpers import get_client_ip


class EventLogger:
    @staticmethod
    def _safe_create(user, ip_address, event_type, detail=''):
        try:
            BotEvent.objects.create(
                user=user,
                ip_address=ip_address,
                event_type=event_type,
                detail=detail,
            )
        except Exception:
            pass

    @staticmethod
    def log_throttled(request, detail=''):
        user = request.user if request.user.is_authenticated else None
        EventLogger._safe_create(
            user=user,
            ip_address=get_client_ip(request),
            event_type=BotEvent.EventType.THROTTLED,
            detail=detail,
        )

    @staticmethod
    def log_failed_login(request, username=''):

        EventLogger._safe_create(
            user=None,
            ip_address=get_client_ip(request),
            event_type=BotEvent.EventType.FAILED_LOGIN,
            detail=f"attempted username: {username}",
        )

    @staticmethod
    def log_signup(request, user):
        EventLogger._safe_create(
            user=user,
            ip_address=get_client_ip(request),
            event_type=BotEvent.EventType.SIGNUP,
            detail="account created",
        )

    @staticmethod
    def log_login(request, user):
        EventLogger._safe_create(
            user=user,
            ip_address=get_client_ip(request),
            event_type=BotEvent.EventType.LOGIN,
            detail="successful login",
        )