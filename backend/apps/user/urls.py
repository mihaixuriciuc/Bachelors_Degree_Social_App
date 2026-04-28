from django.urls import path
from apps.user  import views



urlpatterns = [
    path('all', views.getAllUsers, name='all'),
    path('signUp', views.singUpUser, name='singUp'),
    path('signIn',views.signInUser, name='signIn'),
    path('signIn/refresh',views.signInUser,name='signIn'),



]
