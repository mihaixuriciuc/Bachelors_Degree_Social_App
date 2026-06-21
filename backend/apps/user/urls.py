from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user import views

urlpatterns = [

    path('signUp/', views.singUpUser, name='sign-up'),
    path('signIn/', views.signInUser, name='sign-in'),
    path('signIn/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', views.logOutUser, name='logout'),


    path('activate/<str:uidb64>/<str:token>/', views.verifyEmail, name='activate'),


    path('password-reset/request/', views.requestPasswordReset, name='password-reset-request'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.confirmPasswordReset, name='password-reset-confirm'),


    path('profile/update/', views.updateMyProfile, name='update-profile'),
    path('security/update/', views.updateMySecurity, name='update-security'),

    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/search/', views.searchUsers, name='user-search'),
    path('users/<str:username>/follow/', views.followUser, name='follow-user'),
    path('users/<str:username>/followers/', views.getFollowers, name='user-followers'),
    path('users/<str:username>/following/', views.getFollowing, name='user-following'),
    path('users/<str:username>/', views.getUserProfile, name='user-profile'),
]