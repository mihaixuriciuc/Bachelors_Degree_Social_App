from rest_framework import serializers

from .models import Profile, Follow


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



class ProfileResponseSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    is_staff = serializers.ReadOnlyField(source='user.is_staff')
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'last_name', 'email', 'bio', 'is_staff',
            'profile_pic', 'website', 'followers_count', 'following_count',
        ]
        read_only_fields = fields

    def get_followers_count(self, profile):

        return profile.user.followers.count()

    def get_following_count(self, profile):

        return profile.user.following.count()


class PublicProfileSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(
                follower=request.user,
                following=profile.user,
            ).exists()
        return False


class UserListItemSerializer(serializers.Serializer):
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