from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #model and fields are from Meta annotation
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

        extra_kwargs = {'password': {'write_only': True},'id': {'read_only': True}, 'is_staff': {'read_only': True},'is_superuser': {'read_only': True}}


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
