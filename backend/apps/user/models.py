from django.db import models #the database methods
from django.contrib.auth.models import AbstractUser #the security methods


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True) #sets email to unique
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     #links the user and the profile
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)     #the photo stored locally, null for database and blank for frontend(allows them to be empty)
    bio = models.TextField(null=True, blank=True)               #same here
    website = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.user.username



