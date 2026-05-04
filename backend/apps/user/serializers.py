from rest_framework import serializers
from .models import User, Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #model and fields are from Meta annotation
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

        extra_kwargs = {'password': {'write_only': True},'id': {'read_only': True}, 'is_staff': {'read_only': True},'is_superuser': {'read_only': True}}


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

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