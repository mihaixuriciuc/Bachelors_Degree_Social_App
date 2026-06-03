from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Profile
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileResponseSerializer,
    UpdateProfileSerializer,
    UpdateSecuritySerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from .services import AuthService, ProfileService, UserService


@api_view(['POST'])
@permission_classes([AllowAny])
def singUpUser(request):
    input_serializer = UserRegistrationSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    try:
        user = UserService.register_user(
            username=input_serializer.validated_data['username'],
            email=input_serializer.validated_data['email'],
            password=input_serializer.validated_data['password'],
        )
        AuthService.send_activation_email(user)
        return Response(
            {"message": "Please check your email to activate your account."},
            status=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def signInUser(request):
    input_serializer = UserLoginSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    try:
        auth_data = AuthService.login(
            username=input_serializer.validated_data['username'],
            password=input_serializer.validated_data['password'],
        )

        response = Response(
            {"status": "success", "username": auth_data["username"]},
            status=status.HTTP_200_OK,
        )
        response.set_cookie('access_token', value=auth_data["access_token"], httponly=True, samesite='Lax')
        response.set_cookie('refresh_token', value=auth_data["refresh_token"], httponly=True, samesite='Lax')
        return response
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logOutUser(request):
    response = Response({"status": "success", "message": "Logged out"}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def verifyEmail(request, uidb64, token):
    try:
        AuthService.verify_email(uidb64, token)
        return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def requestPasswordReset(request):
    input_serializer = PasswordResetRequestSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    AuthService.request_password_reset(input_serializer.validated_data['email'])
    return Response(
        {"message": "If an account exists, a reset link has been sent."},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmPasswordReset(request, uidb64, token):
    input_serializer = PasswordResetConfirmSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    try:
        AuthService.confirm_password_reset(
            uidb64=uidb64,
            token=token,
            new_password=input_serializer.validated_data['new_password'],
        )
        return Response(
            {"message": "Password reset successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyProfile(request):
    # With the post_save signal, Profile is auto-created for new users.
    # get_or_create is still used as a safety net for users created
    # before the signal was added.
    profile, _ = Profile.objects.get_or_create(user=request.user)
    output_serializer = ProfileResponseSerializer(profile)
    return Response(output_serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateMyProfile(request):
    input_serializer = UpdateProfileSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    try:
        profile = ProfileService.update_profile(
            request.user,
            **input_serializer.validated_data,
        )
        output_serializer = ProfileResponseSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateMySecurity(request):
    input_serializer = UpdateSecuritySerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    data = input_serializer.validated_data

    try:
        UserService.update_credentials(
            user=request.user,
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
        )

        if data.get('new_password') and data.get('confirm_password'):
            UserService.update_password(
                user=request.user,
                new_password=data['new_password'],
                confirm_password=data['confirm_password'],
            )

        return Response(
            {"message": "Security info updated successfully."},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
