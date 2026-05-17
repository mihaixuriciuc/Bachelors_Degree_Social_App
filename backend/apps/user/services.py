from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, User
from .tokens import TokenService


class ProfileService:
    """Handles public-facing profile data (bio, website, profile picture)."""

    @staticmethod
    def get_or_create_profile(user: User) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def update_profile(
        user: User,
        bio: str = None,
        website: str = None,
        profile_pic=None,
    ) -> Profile:
        profile = ProfileService.get_or_create_profile(user)

        if bio is not None:
            profile.bio = bio
        if website is not None:
            profile.website = website
        if profile_pic is not None:
            profile.profile_pic = profile_pic

        profile.save()
        return profile


class UserService:
    """Handles user identity: username, email, password, first/last name."""

    @staticmethod
    def validate_new_password(password: str, user: User = None) -> None:
        """
        Runs the password through Django's AUTH_PASSWORD_VALIDATORS from settings.py.

        Previously this was a manual check: len(password) < 8 or no digit.
        That approach meant your settings.py validators were configured but
        never actually used — a Dependency Inversion violation.  The settings
        declare the *abstraction* (what rules apply); the service should depend
        on that abstraction, not re-implement its own rules.

        Django's validators give you: minimum length, common-password check,
        numeric-only check, and user-attribute-similarity check — all for free.
        """
        try:
            validate_password(password, user=user)
        except DjangoValidationError as exc:
            # exc.messages is a list like ['This password is too short.', ...]
            # We join them into a single string for our ValueError convention.
            raise ValueError(' '.join(exc.messages))

    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        if User.objects.filter(username=username).exists():
            raise ValueError("This username is already taken.")
        if User.objects.filter(email=email).exists():
            raise ValueError("This email is already registered.")

        # Validate the password using Django's built-in validators.
        UserService.validate_new_password(password)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
        )
        return user

    @staticmethod
    def update_credentials(
        user: User,
        username: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> None:
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                raise ValueError("This username is already taken.")
            user.username = username

        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                raise ValueError("This email is already registered.")
            user.email = email

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        user.save()

    @staticmethod
    def update_password(user: User, new_password: str, confirm_password: str) -> None:
        if new_password != confirm_password:
            raise ValueError("The passwords do not match.")

        UserService.validate_new_password(new_password, user=user)

        user.set_password(new_password)
        user.save()


class AuthService:
    """
    Handles login tokens and email-based flows (activation, password reset).

    Notice how the uid/token encode-decode logic is now in TokenService.
    Before, each method had its own copy of urlsafe_base64_encode/decode +
    force_bytes/force_str + make_token/check_token.  That was four copies
    of the same five lines.  Now each method is shorter and you can't
    accidentally use different encoding in one flow vs another.
    """

    @staticmethod
    def login(username: str, password: str) -> dict:
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("Invalid username or password.")

        refresh = RefreshToken.for_user(user)
        return {
            "username": user.username,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "is_active": user.is_active,
        }

    @staticmethod
    def send_activation_email(user: User) -> None:
        uid = TokenService.encode_uid(user)
        token = TokenService.make_token(user)
        link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}"

        send_mail(
            subject="Confirm your DOT8 Account",
            message=f"Hi {user.username},\nClick here to activate your account: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    @staticmethod
    def verify_email(uidb64: str, token: str) -> None:
        user = TokenService.decode_uid(uidb64)
        TokenService.check_token(user, token)
        user.is_active = True
        user.save()

    @staticmethod
    def request_password_reset(email: str) -> None:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return

        uid = TokenService.encode_uid(user)
        token = TokenService.make_token(user)
        link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            subject="Reset your DOT8 Password",
            message=f"Click the link to reset your password:\n{link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    @staticmethod
    def confirm_password_reset(uidb64: str, token: str, new_password: str) -> None:
        user = TokenService.decode_uid(uidb64)
        TokenService.check_token(user, token)

        UserService.validate_new_password(new_password, user=user)

        user.set_password(new_password)
        user.save()