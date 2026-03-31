from django.urls import path
from apps.user  import views



urlpatterns = [
    path('all', views.getAllUsers, name='all'),
    path('signup', views.singUpUser, name='singUp'),


]
