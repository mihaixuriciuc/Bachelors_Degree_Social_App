from django.urls import path
from apps.user import views


urlpatterns = [
    path('all',views.getAllUsers,name='all'),
    path('singUp' , views.singUpUser,name='singUp'),

]
