from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from apps.bot_detection.services import EventLogger
from apps.user.models import User

from .models import Profile, User
from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileResponseSerializer,
    PublicProfileSerializer,
    UpdateProfileSerializer,
    UpdateSecuritySerializer,
    UserListItemSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from .services import AuthService, FollowService, ProfileService, UserService


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
        EventLogger.log_signup(request, user)
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
        try:
            logged_in_user = User.objects.get(username=auth_data["username"])
            EventLogger.log_login(request, logged_in_user)
        except User.DoesNotExist:
            pass

        response = Response(
            {"status": "success", "username": auth_data["username"]},
            status=status.HTTP_200_OK,
        )
        response.set_cookie('access_token', value=auth_data["access_token"], httponly=True, samesite='Lax')
        response.set_cookie('refresh_token', value=auth_data["refresh_token"], httponly=True, samesite='Lax')
        return response
    except ValueError as e:
        EventLogger.log_failed_login(
            request,
            username=input_serializer.validated_data.get('username', ''),
        )
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


# --- Public profiles & follow system ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request, username):
    """Public profile of any user, looked up by username."""
    target = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=target)
    # context={'request': request} is what lets the serializer compute
    # is_following (it needs to know who is asking).
    serializer = PublicProfileSerializer(profile, context={'request': request})
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def followUser(request, username):

    try:
        if request.method == 'POST':
            FollowService.follow_user(request.user, username)
            return Response(
                {"message": f"You are now following {username}."},
                status=status.HTTP_201_CREATED,
            )
        # DELETE
        FollowService.unfollow_user(request.user, username)
        return Response(
            {"message": f"You have unfollowed {username}."},
            status=status.HTTP_200_OK,
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowers(request, username):

    target = get_object_or_404(User, username=username)
    follows = target.followers.select_related('follower__profile')
    follower_users = [f.follower for f in follows]

    serializer = UserListItemSerializer(
        follower_users, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowing(request, username):

    target = get_object_or_404(User, username=username)

    follows = target.following.select_related('following__profile')
    following_users = [f.following for f in follows]

    serializer = UserListItemSerializer(
        following_users, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):

    query = request.query_params.get('q', '').strip()

    if not query:
        return Response([])

    matches = (
        User.objects
        .filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        .exclude(id=request.user.id)

        .select_related('profile')

        [:10]
    )

    serializer = UserListItemSerializer(
        matches, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    """
    Permanently delete a user account and all their data.
    Cascades to posts, comments, likes, follows, and bot events via the
    on_delete=CASCADE foreign keys. Irreversible — the frontend confirms
    before calling this.

    Guards against an admin deleting a staff account (including themselves)
    by accident.
    """
    user = get_object_or_404(User, id=user_id)

    if user.is_staff:
        return Response(
            {"error": "Cannot delete staff accounts."},
            status=status.HTTP_403_FORBIDDEN,
        )

    username = user.username
    user.delete()  # cascades to all related data
    return Response(
        {"message": f"Account '{username}' permanently deleted."},
        status=status.HTTP_200_OK,
    )