from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_init, post_save
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Profile(models.Model):
    """
        user profile
    """
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_slug = models.SlugField()

    def __str__(self):
        return str(self._meta.get_fields(include_hidden=True))


"""
    Custom signals to create and update user profile
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)
        instance.profile.user_slug = slugify(instance.username)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()
