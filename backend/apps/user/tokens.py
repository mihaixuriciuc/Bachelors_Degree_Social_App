
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


class TokenService:


    @staticmethod
    def encode_uid(user: User) -> str:

        return urlsafe_base64_encode(force_bytes(user.pk))

    @staticmethod
    def decode_uid(uidb64: str) -> User:

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValueError("Invalid link.")

    @staticmethod
    def make_token(user: User) -> str:

        return default_token_generator.make_token(user)

    @staticmethod
    def check_token(user: User, token: str) -> None:

        if not default_token_generator.check_token(user, token):
            raise ValueError("Link is expired or invalid.")