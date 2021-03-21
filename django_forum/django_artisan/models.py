import os
import uuid
from random import randint
from pathlib import Path

from sorl.thumbnail import delete

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.conf import settings

from django_forum_app.models import ForumProfile, create_user_forum_profile, save_user_forum_profile, Avatar, default_avatar


def user_directory_path(instance, filename):
    if type(instance) is ArtisanForumProfile:
        return 'uploads/users/{0}/{1}'.format(instance.display_name, filename)
    else:
        return 'uploads/users/{0}/{1}'.format(instance.user_profile.display_name, filename)


class ArtisanForumProfile(ForumProfile):
    bio = models.TextField('biographical information, max 500 chars', 
                            max_length=500, 
                            blank=True, 
                            default='', 
                            help_text="This is the biographical information that will be presented on your personal page")
    image_file = models.ImageField('A single image for your personal page', upload_to=user_directory_path, null=True)
    shop_web_address = models.CharField('shop link', max_length=50, blank=True, default='')
    outlets = models.CharField('places that sell my stuff, comma separated', max_length=400, blank=True, default='')
    listed_member = models.BooleanField('List me on about page', default=False)
    display_personal_page = models.BooleanField('Display personal page', default=False)
"""
    disconnect dummy profile
"""
post_save.disconnect(create_user_forum_profile, sender=User)
post_save.disconnect(save_user_forum_profile, sender=User)
"""
    Custom signals to create and update user profile
"""
@receiver(post_save, sender=User)
def create_user_artisan_forum_profile(sender, instance, created, **kwargs):
    if created:
        ArtisanForumProfile.objects.create(profile_user=instance, 
                                    avatar=Avatar.objects.create(
                                        image_file=default_avatar(randint(1,4))))
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_artisan_forum_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except (ObjectDoesNotExist, FieldError):
        pass
        ## TODO: log error to log file.

@receiver(pre_delete, sender=ArtisanForumProfile)
def auto_delete_image_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
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

                except ObjectDoesNotExist as i:
                    # TODO: log file missing
                    pass


# TODO: validate image_shop_link properly 
# TODO: set a default of 
class UserProductImage(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path)
    image_text = models.CharField(max_length=400, default='', blank=True)
    image_title = models.CharField(max_length=30, default='', blank=True)
    image_shop_link = models.CharField(max_length=50, default='', blank=True)
    image_shop_link_title = models.CharField(max_length=30, default='', blank=True)
    active = models.BooleanField(default=False)
    user_profile = models.ForeignKey(ArtisanForumProfile, on_delete=models.CASCADE, related_name="forum_images")
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.PositiveIntegerField(default=0, editable=False)

    # def __str__(self):
    #     return f"Profile_image:user={self.user_profile.profile_user.username},active={self.active}"

    """
         because I made the primary key a uuid field, I need a way of returning the next logical
         post, as django doesn't allow auto-incrementing integers.  The below method uses transaction.atomic
         with F strings to return a record in a way that won't go wrong even if the database fails.
         https://stackoverflow.com/a/54148942
    """
    @classmethod
    def get_next(cls):
        with transaction.atomic():
            cls.objects.update(id=models.F('id') + 1)
            return cls.objects.values_list('id', flat=True)[0]


@receiver(post_delete, sender=UserProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    fp = instance.image_file.path
    fd = os.path.dirname(fp)
    if instance.image_file:
        delete(instance.image_file)   #removes from cache - sorl thumbnail
        if len(os.listdir(fd)) == 0:
            os.rmdir(fd)

@receiver(pre_save, sender=UserProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image_field = UserProductImage.objects.get(pk=instance.pk)
    except UserProductImage.DoesNotExist:
        return False

    new_file = instance.image_file
    if not old_image_field.file == new_file:
        if os.path.isfile(old_image_field.file.path):
            delete(old_image_field) # clear thumbs from cache
            os.remove(old_image_field.file.path)


class Event(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=400)
    time = models.TimeField(auto_now_add=False)
    every = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField(auto_now_add=False, blank=True, null=True)
    repeating = models.BooleanField(default=False)
    active = models.BooleanField(default=True)