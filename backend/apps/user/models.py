from django.db import models  # the database methods
from django.contrib.auth.models import AbstractUser  # the security methods

from apps.user.helpers import user_directory_path


class User(AbstractUser):
    email = models.EmailField(unique=True)  # sets email to unique
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # links the user and the profile
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    """
    A directed follow relationship: `follower` follows `following`.

    The related_name values are the confusing part, so read carefully:

    - `follower` is the user DOING the following.
      related_name='following' means `some_user.following.all()` returns the
      Follow rows where `some_user` is the follower → "the people I follow".

    - `following` is the user BEING followed.
      related_name='followers' means `some_user.followers.all()` returns the
      Follow rows where `some_user` is being followed → "the people who follow me".

    Example: a row with follower=Alice, following=Bob means "Alice follows Bob".
      - Alice.following  → includes this row (Alice follows Bob)
      - Bob.followers    → includes this row (Bob is followed by Alice)
    """
    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can't follow the same person twice — enforced at the DB level.
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"