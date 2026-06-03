"""
Centralizes one-time-token logic used by email activation and password reset.

Before this file existed, the same five-line uid-encode / uid-decode / token-make
/ token-check dance was copy-pasted across four methods in AuthService.  If the
encoding scheme ever changed (e.g., switching from base64 to a signed payload),
you'd have to update all four copies — and miss one.

This is the DRY principle in action: extract the repeated pattern into one place,
then call it from everywhere.
"""

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


class TokenService:
    """
    Handles encoding/decoding user IDs for URL-safe links, and
    generating/verifying one-time tokens tied to a user's state.
    """

    @staticmethod
    def encode_uid(user: User) -> str:
        """
        Turns a user's primary key into a URL-safe base64 string.
        Example: user.pk = 42  →  'NDI='  (but URL-safe, no slashes or plus signs).
        """
        return urlsafe_base64_encode(force_bytes(user.pk))

    @staticmethod
    def decode_uid(uidb64: str) -> User:
        """
        Reverses encode_uid: takes the base64 string from the URL and returns
        the User object.  Raises ValueError if the string is malformed or
        the user doesn't exist.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValueError("Invalid link.")

    @staticmethod
    def make_token(user: User) -> str:
        """
        Generates a one-time-use token tied to the user's current state.
        The token is derived from the user's password hash + last login
        timestamp + a secret key, so it automatically invalidates when
        the user changes their password or logs in again.
        """
        return default_token_generator.make_token(user)

    @staticmethod
    def check_token(user: User, token: str) -> None:
        """
        Verifies the token against the user's current state.
        Raises ValueError if the token is expired or invalid.
        """
        if not default_token_generator.check_token(user, token):
            raise ValueError("Link is expired or invalid.")