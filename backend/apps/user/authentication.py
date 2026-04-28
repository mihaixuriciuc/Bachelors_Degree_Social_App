from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if not raw_token:
            return None
        validated_token = self.get_validated_token(raw_token)
        logged_user = self.get_user(validated_token)
        response = ( logged_user,validated_token)
        return response


