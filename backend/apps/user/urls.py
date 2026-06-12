from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user import views

urlpatterns = [
    # Auth
    path('signUp/', views.singUpUser, name='sign-up'),
    path('signIn/', views.signInUser, name='sign-in'),
    path('signIn/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.logOutUser, name='logout'),

    # Email activation
    path('activate/<str:uidb64>/<str:token>/', views.verifyEmail, name='activate'),

    # Password reset flow
    path('password-reset/request/', views.requestPasswordReset, name='password-reset-request'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.confirmPasswordReset, name='password-reset-confirm'),

    # Own profile & security
    path('profile/update/', views.updateMyProfile, name='update-profile'),
    path('security/update/', views.updateMySecurity, name='update-security'),

    # Public profiles & follow system.
    # More specific routes (follow/followers/following) are listed before the
    # bare profile route. Django's <str:username> won't match a path containing
    # a slash anyway, so there's no real conflict, but ordering this way is
    # clearer to read.
    path('users/search/', views.searchUsers, name='user-search'),
    path('users/<str:username>/follow/', views.followUser, name='follow-user'),
    path('users/<str:username>/followers/', views.getFollowers, name='user-followers'),
    path('users/<str:username>/following/', views.getFollowing, name='user-following'),
    path('users/<str:username>/', views.getUserProfile, name='user-profile'),
]