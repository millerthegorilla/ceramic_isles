import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_init, pre_save, post_save, post_delete
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

"""
   function to define directory path
"""
def user_directory_path(instance, filename):
    return 'uploads/users/{0}/{1}'.format(instance.user_profile.profile_user, filename)


class ProfileImage(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="images")
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.PositiveIntegerField(default=0, editable=False)

    @classmethod
    def get_next(cls):
        with transaction.atomic():
            cls.objects.update(id=models.F('id') + 1)
            return cls.objects.values_list('id', flat=True)[0]


@receiver(post_delete, sender=ProfileImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)

@receiver(pre_save, sender=ProfileImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image_field = ProfileImage.objects.get(pk=instance.pk)
    except ProfileImage.DoesNotExist:
        return False

    new_file = instance.image_file
    if not old_image_field.file == new_file:
        if os.path.isfile(old_image_field.file.path):
            os.remove(old_image_field.file.path)
