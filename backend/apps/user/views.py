from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProfileSerializer
from .models import User, Profile
from .serializers import UserSerializerSignIn, UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings


# ... keep your existing imports ...

@api_view(['POST'])
def singUpUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # 1. Save the user, but don't activate them yet
        user = serializer.save(is_active=False)

        # 2. Generate a secure token and encode the user's ID
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # 3. Create the activation link (This points to your React frontend!)
        activation_link = f"http://localhost:5173/activate/{uid}/{token}"

        # 4. Send the email
        send_mail(
            subject="Confirm your DOT8 Account",
            message=f"Hi {user.username},\n\nPlease click the link below to activate your account:\n{activation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({
            "status": "success",
            "message": "Please check your email to activate your account."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 👇 NEW: Verify Email View 👇
@api_view(['POST'])
def verifyEmail(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if user exists and token is valid
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account activated successfully! You can now log in."}, status=status.HTTP_200_OK)

    return Response({"error": "Activation link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


# 👇 NEW: Request Password Reset View 👇
@api_view(['POST'])
def requestPasswordReset(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Points to a "Reset Password" page on your React frontend
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

        send_mail(
            subject="Reset your DOT8 Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except User.DoesNotExist:
        # We don't reveal if the email exists or not for security reasons!
        pass

    return Response({"message": "If an account with that email exists, a reset link has been sent."},
                    status=status.HTTP_200_OK)


# 👇 NEW: Confirm Password Reset View 👇
@api_view(['POST'])
def confirmPasswordReset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')

        # Validate length/numbers manually here or use a serializer
        if len(new_password) < 8 or not any(char.isdigit() for char in new_password):
            return Response({"error": "Password must be at least 8 characters and contain a number."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully. You can now log in."}, status=status.HTTP_200_OK)

    return Response({"error": "Reset link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


# ... keep your existing updateMyProfile and updateMySecurity views below ...
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



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyProfile(request):
    # 'request.user' automatically holds the user who owns the JWT token!
    user = request.user

    # Find the Profile, or create one if it doesn't exist yet (useful for new signups)
    profile, created = Profile.objects.get_or_create(user=user)

    # Serialize it and return the Response!
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
def logOutUser(request):
    response = Response({"status": "success", "message": "Logged out"}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateMyProfile(request):
    # Get the existing profile
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Pass the instance AND the data. partial=True allows updating just 1 or 2 fields
    serializer = ProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 👇 2. Updates first_name, last_name, email, and password 👇
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateMySecurity(request):
    user = request.user

    # Uses the UserSerializer we just updated
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "Security info updated successfully."
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)