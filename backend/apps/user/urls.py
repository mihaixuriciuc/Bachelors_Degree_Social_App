from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user import views

urlpatterns = [
    # Auth
    path('signUp/', views.singUpUser, name='sign-up'),
    path('signIn/', views.signInUser, name='sign-in'),
    # TokenRefreshView reads the refresh_token, validates it, and issues a new access_token.
    # Your old code pointed this at signInUser which just tried to log in — wrong.
    path('signIn/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.logOutUser, name='logout'),

    # Email activation
    path('activate/<str:uidb64>/<str:token>/', views.verifyEmail, name='activate'),

    # Password reset flow
    path('password-reset/request/', views.requestPasswordReset, name='password-reset-request'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.confirmPasswordReset, name='password-reset-confirm'),

    # Profile & security
    path('profile/update/', views.updateMyProfile, name='update-profile'),
    path('security/update/', views.updateMySecurity, name='update-security'),
]