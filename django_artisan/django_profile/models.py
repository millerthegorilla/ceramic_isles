import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_init, pre_save, post_save, post_delete
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


def get_default_display_name():
    return str(uuid.uuid4())


# Create your models here.
class Profile(models.Model):
    """
        user profile
    """
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=37, blank=True, unique=True, default=get_default_display_name())

    def __str__(self):
        return str(self._meta.get_fields(include_hidden=True))


"""
    Custom signals to create and update user profile
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()
