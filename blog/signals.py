# Django Imports
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


# Creates a user profile automatically
# When someone signs up as a new user, their profile is set up automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a user profile automatically when a new user is created
    Input values:
        sender: The User model that triggered this action
        instance: The specific user being created
        created: True/False to indicate if this is a new user
        **kwargs: Any extra settings (optional)
    """
    if created:
        UserProfile.objects.create(user=instance)
# Automatically updates the user's profile
# When the main user information is saved, their profile details are also saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically saves user profile changes.
    Required parameters:
    sender: User model trigger
    instance: User being updated
    **kwargs: Extra parameters passed in
    """
    instance.userprofile.save()
