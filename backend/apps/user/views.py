from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q

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
    """
    POST   -> follow the user
    DELETE -> unfollow the user

    One view handles both because they're the same resource (a follow
    relationship) being created or destroyed.
    """
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
    """List the users who follow `username`."""
    target = get_object_or_404(User, username=username)

    # target.followers = Follow rows where target is being followed.
    # Each row's .follower is a user who follows target.
    # select_related('follower__profile') prefetches the follower AND their
    # profile in one query so the serializer's profile_pic lookup is free.
    follows = target.followers.select_related('follower__profile')
    follower_users = [f.follower for f in follows]

    serializer = UserListItemSerializer(
        follower_users, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowing(request, username):
    """List the users that `username` follows."""
    target = get_object_or_404(User, username=username)

    # target.following = Follow rows where target is the follower.
    # Each row's .following is a user that target follows.
    follows = target.following.select_related('following__profile')
    following_users = [f.following for f in follows]

    serializer = UserListItemSerializer(
        following_users, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    """
    Search users by username, first name, or last name.

    The query comes in as ?q=alice in the URL. We read it from
    request.query_params (DRF's version of request.GET).
    """
    query = request.query_params.get('q', '').strip()

    # Don't search on an empty string — that would return every user.
    if not query:
        return Response([])

    # Q objects let you build OR conditions. Without Q you can only AND
    # filters together. Here we want: username contains q OR first_name
    # contains q OR last_name contains q.
    #
    # __icontains means "case-insensitive contains" — searching "ali"
    # matches "Alice", "aalimov", "natalia", etc.
    matches = (
        User.objects
        .filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        # Don't include the person doing the searching in their own results.
        .exclude(id=request.user.id)
        # select_related('profile') so the serializer's profile_pic lookup
        # doesn't fire a separate query per result (N+1).
        .select_related('profile')
            # Cap the results so a broad search doesn't return thousands of rows.
        [:10]
    )

    serializer = UserListItemSerializer(
        matches, many=True, context={'request': request}
    )
    return Response(serializer.data)