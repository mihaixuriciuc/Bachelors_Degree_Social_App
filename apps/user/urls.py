from django.urls import path
from apps.user import views


urlpatterns = [
    path('all/',views.getUserJson,name='all'),
    path('singUp/' , views.createUser,name='singUp')
]
