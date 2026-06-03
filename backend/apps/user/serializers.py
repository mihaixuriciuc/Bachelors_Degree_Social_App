from rest_framework import serializers

from .models import Profile


# --- INPUT serializers (validate what comes IN from the client) ---

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UpdateProfileSerializer(serializers.Serializer):
    # These fields map directly to the Profile model.
    # first_name / last_name are on the User model, NOT Profile —
    # they belong in UpdateSecuritySerializer and are handled there.
    bio = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)


class UpdateSecuritySerializer(serializers.Serializer):
    # first_name and last_name live on the User model, so they are
    # security/identity fields, not profile fields.
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
    # Pull user fields through the OneToOne relation.
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'profile_pic', 'website']
        read_only_fields = fields