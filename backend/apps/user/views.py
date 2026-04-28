from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializerSignIn, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def singUpUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        answer = {"status": "success",
                  "username": user.username
        }

        response = Response(answer, status=status.HTTP_201_CREATED)
        response.set_cookie('access_token', value=str(refresh.access_token), httponly=True)
        response.set_cookie('refresh_token', value=str(refresh), httponly=True)
        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signInUser(request):
    serializer = UserSerializerSignIn(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:

            refresh = RefreshToken.for_user(user)

            answer = {"status": "success",
                      "username": user.username
                      }

            response = Response(answer, status=status.HTTP_200_OK)
            response.set_cookie('access_token', value=str(refresh.access_token), httponly=True)
            response.set_cookie('refresh_token', value=str(refresh), httponly=True)
            return response
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)