from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CustomCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')

        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            # Token exists but is expired or invalid.
            # Return None instead of raising — this lets AllowAny endpoints
            # still work even when the browser has a stale cookie.
            return None

        logged_user = self.get_user(validated_token)
        return (logged_user, validated_token)