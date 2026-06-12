from rest_framework import serializers

from .models import Profile, Follow


# --- INPUT serializers (validate what comes IN from the client) ---

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UpdateProfileSerializer(serializers.Serializer):
    bio = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)


class UpdateSecuritySerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)
    new_password = serializers.CharField(required=False, write_only=True)
    confirm_password = serializers.CharField(required=False, write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


# --- OUTPUT serializers (format what goes OUT to the client) ---

class ProfileResponseSerializer(serializers.ModelSerializer):
    """
    The logged-in user's OWN profile. Includes the email (private) and
    the follower/following counts.
    """
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'last_name', 'email', 'bio',
            'profile_pic', 'website', 'followers_count', 'following_count',
        ]
        read_only_fields = fields

    def get_followers_count(self, profile):
        # profile.user.followers = Follow rows where this user is followed.
        return profile.user.followers.count()

    def get_following_count(self, profile):
        # profile.user.following = Follow rows where this user is the follower.
        return profile.user.following.count()


class PublicProfileSerializer(serializers.ModelSerializer):
    """
    For viewing ANOTHER user's profile. Same as the own-profile serializer
    but WITHOUT the email (privacy), plus an `is_following` flag so the
    frontend knows whether to show "Follow" or "Following".
    """
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'last_name', 'bio', 'profile_pic',
            'website', 'followers_count', 'following_count', 'is_following',
        ]
        read_only_fields = fields

    def get_followers_count(self, profile):
        return profile.user.followers.count()

    def get_following_count(self, profile):
        return profile.user.following.count()

    def get_is_following(self, profile):
        # Does the currently logged-in user follow the profile being viewed?
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user,
                following=profile.user,
            ).exists()
        return False


class UserListItemSerializer(serializers.Serializer):
    """
    A compact user representation for follower/following lists.
    Just enough to render a clickable row: username, first name, picture.

    This is a plain Serializer (not ModelSerializer) because it takes a
    User instance directly and reaches into the related Profile for the
    picture. The view should select_related('profile') to avoid N+1 queries.
    """
    username = serializers.CharField()
    first_name = serializers.CharField()
    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, user):
        request = self.context.get('request')
        try:
            profile = user.profile  # OneToOne reverse accessor
        except Profile.DoesNotExist:
            return None
        if profile.profile_pic and request:
            return request.build_absolute_uri(profile.profile_pic.url)
        return None