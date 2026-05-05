from rest_framework import serializers
from .models import User, Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #model and fields are from Meta annotation
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

        extra_kwargs = {'password': {'write_only': True},'id': {'read_only': True}, 'is_staff': {'read_only': True},'is_superuser': {'read_only': True}}

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value

    # 👇 2. General Field Validation 👇
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("First name is too short.")
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name is too short.")
        return value
    def validate_email(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Email is too short.")

        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")

        elif "@" not in value:
            raise serializers.ValidationError("Email must have @")
        else:
            return value

    def validate_username(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Username is too short.")
        # Check if username already exists
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")

        return value


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)  # Hashes the new password!

        return super().update(instance, validated_data)

class UserSerializerSignIn(serializers.Serializer):
    # We call it 'identifier' so the user can provide either a username OR an email
    username = serializers.CharField(required=True)

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )


class ProfileSerializer(serializers.ModelSerializer):
    # We can add a ReadOnlyField to grab the username from the related User model.
    # 'user.username' traverses the OneToOneField relationship!
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_pic', 'website']