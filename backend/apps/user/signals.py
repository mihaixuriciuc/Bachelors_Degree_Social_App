from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Runs every time a User is saved.  The 'created' flag tells us
    whether this is a brand-new user (INSERT) or an update.
    We only create a Profile on INSERT.
    """
    if created:
        Profile.objects.create(user=instance)