import os
import uuid
import logging
from random import randint
from pathlib import Path
from typing import Any, Union

from django_q.tasks import async_task
from sorl.thumbnail import delete

from django.contrib.auth.models import User
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, FieldError

from django_profile.models import Profile
from django_forum_app.models import ForumProfile, create_user_forum_profile, save_user_forum_profile, Avatar, default_avatar
from django_forum_app.views import ForumPostView
from safe_imagefield.models import SafeImageField

logger = logging.getLogger('django_artisan')


def user_directory_path(instance : Union['ArtisanForumProfile', 'UserProductImage'], filename: str) -> str:
    if isinstance(instance, ArtisanForumProfile):
        return 'uploads/users/{0}/{1}'.format(
            instance.display_name, filename)
    else:
        return 'uploads/users/{0}/{1}'.format(
            instance.user_profile.display_name, filename)


class ArtisanForumProfile(ForumProfile):
    bio: models.TextField = models.TextField('biographical information, max 500 chars',
                           max_length=500,
                           blank=True,
                           default='')
    image_file: models.ImageField = models.ImageField(
        'A single image for your personal page',
        upload_to=user_directory_path,
        null=True,
        blank=True)
    shop_web_address: models.CharField = models.CharField(
        'shop link', max_length=50, blank=True, default='')
    outlets: models.CharField = models.CharField(
        'places that sell my stuff, comma separated',
        max_length=400,
        blank=True,
        default='')
    listed_member: models.BooleanField = models.BooleanField('List me on about page', default=False)
    display_personal_page: models.BooleanField = models.BooleanField(
        'Display personal page', default=False)


"""
    disconnect dummy profile
"""
post_save.disconnect(create_user_forum_profile, sender=User)
post_save.disconnect(save_user_forum_profile, sender=User)
"""
    Custom signals to create and update user profile
"""


@receiver(post_save, sender=User)
def create_user_artisan_forum_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        ArtisanForumProfile.objects.create(
            profile_user=instance,
            avatar=Avatar.objects.create(
                image_file=default_avatar(
                    randint(
                        1,
                        4))))
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_artisan_forum_profile(sender, instance: User, **kwargs):
    try:
        instance.profile.save()
    except (ObjectDoesNotExist, FieldError) as e:
        logger.error("Error saving ArtisanForumProfile : {0}".format(e))


@receiver(pre_delete, sender=ArtisanForumProfile)
def auto_delete_image_file_on_delete(sender: ArtisanForumProfile, instance: ArtisanForumProfile, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.  Typed to SafeImageField as a test (should be ImageField)
    """
    if instance.image_file:
        fp = instance.image_file.path
        fd = os.path.dirname(fp)
        if instance.image_file:
            if os.path.isfile(fp):
                try:
                    delete(instance.image_file)
                    if len(os.listdir(fd)) == 0:
                        os.rmdir(fd)
                    fdu1 = settings.MEDIA_ROOT + \
                        'uploads/users/' + \
                        instance.display_name
                    if os.path.isdir(fdu1):
                        if len(os.listdir(fdu1)) == 0:
                            os.rmdir(fdu1)

                except ObjectDoesNotExist as e:
                    logger.error("Error deleting image file : {0}".format(e))


# TODO: validate image_shop_link properly
# TODO: set a default of
class UserProductImage(models.Model):
    class Meta:
        permissions = [('approve_image', 'Approve Image')]

    image_file: SafeImageField = SafeImageField(upload_to=user_directory_path)
    image_text: models.CharField = models.CharField(max_length=400, default='', blank=True)
    image_title: models.CharField = models.CharField(max_length=30, default='', blank=True)
    image_shop_link: models.CharField = models.CharField(max_length=50, default='', blank=True)
    image_shop_link_title: models.CharField = models.CharField(
        max_length=30, default='', blank=True)
    active: models.BooleanField = models.BooleanField(default=False)
    user_profile: models.ForeignKey = models.ForeignKey(
        ArtisanForumProfile,
        on_delete=models.CASCADE,
        related_name="forum_images")
    image_id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    id: models.PositiveIntegerField = models.PositiveIntegerField(default=0, editable=False)

    # def __str__(self):
    # return
    # f"Profile_image:user={self.user_profile.profile_user.username},active={self.active}"

    """
         because I made the primary key a uuid field, I need a way of returning the next sequential
         image, as django doesn't allow auto-incrementing integers.  The below method uses transaction.atomic
         with F strings to return a record in a way that won't go wrong even if the database fails.
         https://stackoverflow.com/a/54148942
         TODO (returning to code at later date) - 
         - what if primary key returned by get_next refers to an existing object
         https://docs.djangoproject.com/en/3.2/ref/models/instances/ 
    """
    @classmethod
    def get_next(cls) -> int:
        with transaction.atomic():
            cls.objects.update(id=models.F('id') + 1)
            return cls.objects.values_list('id', flat=True)[0]


@receiver(post_delete, sender=UserProductImage)
def auto_delete_file_on_delete(sender: UserProductImage, instance: UserProductImage, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    fp = instance.image_file.path
    fd = os.path.dirname(fp)
    if instance.image_file:
        delete(instance.image_file)  # removes from cache - sorl thumbnail
        if len(os.listdir(fd)) == 0:
            os.rmdir(fd)

# the below function was commented out
@receiver(pre_save, sender=UserProductImage)
def auto_delete_file_on_change(sender: UserProductImage, instance:UserProductImage, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        breakpoint()
        old_image_field = UserProductImage.objects.get(pk=instance.pk)
    except UserProductImage.DoesNotExist as e:
        logger.info("New UserProductImage being installed?: {0}".format(e))
        return False

    new_file = instance.image_file
    if not old_image_field.file == new_file:
        if os.path.isfile(old_image_field.file.path):
            delete(old_image_field) # clear thumbs from cache
            os.remove(old_image_field.file.path)


@receiver(post_save, sender=UserProductImage)
def send_email_when_image_uploaded(sender: UserProductImage, instance: UserProductImage, **kwargs):
    """
       Send email to moderators
    """
    async_task(ForumPostView.send_mod_mail('Image'))


class Event(models.Model):
    title: models.CharField = models.CharField(max_length=50)
    text: models.CharField = models.CharField(max_length=400)
    time: models.TimeField = models.TimeField(auto_now_add=False)
    every: models.CharField = models.CharField(max_length=40, blank=True, null=True)
    date: models.DateField = models.DateField(auto_now_add=False, blank=True, null=True)
    repeating: models.BooleanField = models.BooleanField(default=False)
    active:models.BooleanField = models.BooleanField(default=True)
