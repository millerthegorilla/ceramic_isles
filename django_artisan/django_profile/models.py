from random_username.generate import generate_username

from django import dispatch
from django.db import models
from django.db.models import signals
from django.contrib.auth import models as auth_models


def default_display_name() -> str:
    return generate_username()[0]

# Create your models here.


class Profile(models.Model):
    """
        user profile
    """
    profile_user: models.OneToOneField = models.OneToOneField(
        auth_models.User, on_delete=models.CASCADE, related_name='profile')
    display_name: models.CharField = models.CharField(
        max_length=37, blank=True, unique=True, default=default_display_name)

    def __str__(self) -> str:
        return str(self._meta.get_fields(include_hidden=True))


"""
    Custom signals to create and update user profile
"""


@dispatch.receiver(models.signals.post_save, sender=auth_models.User)
def create_user_profile(sender:auth_models.User, instance:auth_models.User, created:bool, **kwargs) -> None:
    if created:
        Profile.objects.create(profile_user=instance)
    instance.profile.save()


signals.post_save.connect(create_user_profile, sender=auth_models.User)


# @dispatch.receiver(models.signals.post_save, sender=auth_models.User)
# def save_user_profile(sender:auth_models.User, instance:auth_models.User, **kwargs) -> None:
#     if hasattr(instance, 'profile'):
#         instance.profile.save()
