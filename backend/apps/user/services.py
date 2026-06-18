from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile, User, Follow
from .tokens import TokenService


class ProfileService:

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


    @staticmethod
    def validate_new_password(password: str, user: User = None) -> None:

        try:
            validate_password(password, user=user)
        except DjangoValidationError as exc:
            raise ValueError(' '.join(exc.messages))

    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        if User.objects.filter(username=username).exists():
            raise ValueError("This username is already taken.")
        if User.objects.filter(email=email).exists():
            raise ValueError("This email is already registered.")

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


class FollowService:

    @staticmethod
    def _get_user_or_raise(username: str) -> User:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User not found.")

    @staticmethod
    def follow_user(follower: User, username_to_follow: str) -> None:
        target = FollowService._get_user_or_raise(username_to_follow)

        if target == follower:
            raise ValueError("You cannot follow yourself.")

        Follow.objects.get_or_create(follower=follower, following=target)

    @staticmethod
    def unfollow_user(follower: User, username_to_unfollow: str) -> None:
        target = FollowService._get_user_or_raise(username_to_unfollow)
        Follow.objects.filter(follower=follower, following=target).delete()

    @staticmethod
    def is_following(follower: User, target: User) -> bool:
        return Follow.objects.filter(follower=follower, following=target).exists()


class AuthService:

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