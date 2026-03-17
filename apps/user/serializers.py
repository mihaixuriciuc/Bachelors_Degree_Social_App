from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #model and fields are from Meta annotation
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']