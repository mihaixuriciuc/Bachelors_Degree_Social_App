from django.urls import path
from accounts import views


urlpatterns = [
    path('home', views.home, name='home'),
]