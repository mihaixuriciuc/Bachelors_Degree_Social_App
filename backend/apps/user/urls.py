from django.urls import path
from apps.user  import views



urlpatterns = [
    path('all', views.getAllUsers, name='all'),
    path('signUp', views.singUpUser, name='singUp'),
    path('signIn',views.signInUser, name='signIn'),
    path('signIn/refresh',views.signInUser,name='signIn'),
    path('logout', views.logOutUser, name='logout'),
    path('profile/update/', views.updateMyProfile, name='update-profile'),
    path('security/update/', views.updateMySecurity, name='update-security'),
    path('activate/<str:uidb64>/<str:token>/', views.verifyEmail, name='activate'),
    path('password-reset/request/', views.requestPasswordReset, name='password-reset-request'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', views.confirmPasswordReset, name='password-reset-confirm'),




]
