import os, uuid, logging, shutil, typing
from uuid import UUID
from random import randint

from django_q import tasks
from sorl import thumbnail

from django import conf, urls
from django.contrib.auth import models as auth_models
from django.db import models, transaction
from django.dispatch import receiver
from django.db.models import signals
from django.core import exceptions

from django_forum import models as forum_models
from django_forum import views as forum_views
from django_forum import views_forum_post as forum_post_views

from safe_imagefield import models as safe_image_models

logger = logging.getLogger('django_artisan')


class Post(forum_models.Post):
    category: models.CharField = models.CharField(
        max_length=2,
        choices=conf.settings.CATEGORY.choices,
        default=conf.settings.CATEGORY.GENERAL,
    )

    location: models.CharField = models.CharField(
        max_length=2,
        choices=conf.settings.LOCATION.choices,
        default=conf.settings.LOCATION.ANY_ISLE,
    )

    def category_label(self) -> str:
        return conf.settings.CATEGORY(self.category).label

    def location_label(self) -> str:
        return conf.settings.LOCATION(self.location).label

    def get_absolute_url(self, a_name='django_artisan') -> str:
        return urls.reverse_lazy(
            a_name + ':post_view',
            args=[self.id, self.slug]) # type: ignore


"""
   for upload_to in UserProductImage and ArtisanForumProfile
"""
def user_directory_path(instance : typing.Union['ArtisanForumProfile', 'UserProductImage'], filename: str) -> str:
    if isinstance(instance, ArtisanForumProfile):
        return 'uploads/users/{0}/{1}'.format(
            instance.display_name, filename)
    else:
        return 'uploads/users/{0}/{1}'.format(
            instance.user_profile.display_name, filename)


class ArtisanForumProfile(forum_models.ForumProfile):
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
signals.post_save.disconnect(forum_models.create_user_forum_profile, sender=auth_models.User)
#signals.post_save.disconnect(forum_models.save_user_forum_profile, sender=auth_models.User)

"""
    Custom signals to create and update user profile
"""
@receiver(signals.post_save, sender=auth_models.User)
def create_user_artisan_forum_profile(sender, instance: auth_models.User, created: bool = False, **kwargs):
    if created:
        ArtisanForumProfile.objects.create(
            profile_user=instance,
            avatar=forum_models.Avatar.objects.create(
                image_file=forum_models.default_avatar(
                    randint(
                        1,
                        4))))
    try:
        instance.profile.save()
    except (exceptions.ObjectDoesNotExist, exceptions.FieldError) as e:
        logger.error("Error saving ArtisanForumProfile : {0}".format(e))

# @receiver(signals.post_save, sender=auth_models.User)
# def save_user_artisan_forum_profile(sender, instance: auth_models.User, **kwargs):
#     breakpoint()
#     try:
#         instance.profile.save()
#     except (exceptions.ObjectDoesNotExist, exceptions.FieldError) as e:
#         logger.error("Error saving ArtisanForumProfile : {0}".format(e))

signals.post_save.connect(create_user_artisan_forum_profile, sender=auth_models.User)
#signals.pre_save.connect(save_user_artisan_forum_profile, sender=auth_models.User)

"""
    Custom signal to delete underlying filesystem image file
"""
@receiver(signals.pre_delete, sender=ArtisanForumProfile)
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
                    thumbnail.delete(instance.image_file)
                    if len(os.listdir(fd)) == 0:
                        shutil.rmtree(conf.settings.MEDIA_ROOT + '/' + instance.user_profile.display_name, ignore_errors=True)
                    # fdu1 = core.settings.MEDIA_ROOT + \
                    #     'uploads/users/' + \
                    #     instance.display_name
                    # if os.path.isdir(fdu1):
                    #     if len(os.listdir(fdu1)) == 0:
                    #         os.rmdir(fdu1)

                except exceptions.ObjectDoesNotExist as e:
                    logger.error("Error deleting image file : {0}".format(e))


# TODO: validate image_shop_link properly
# TODO: set a default of
class UserProductImage(models.Model):
    class Meta:
        permissions = [('approve_image', 'Approve Image')]

    image_file: safe_image_models.SafeImageField = safe_image_models.SafeImageField(upload_to=user_directory_path, max_length=250)
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
    image_id: models.UUIDField = models.UUIDField(default=uuid.uuid4, editable=False)

@receiver(signals.post_delete, sender=UserProductImage)
def auto_delete_file_on_delete(sender: UserProductImage, instance: UserProductImage, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    fp = instance.image_file.path
    fd = os.path.dirname(fp)
    if instance.image_file:
        thumbnail.delete(instance.image_file)  # removes from cache - sorl thumbnail
        if len(os.listdir(fd)) == 0:
            shutil.rmtree(conf.settings.MEDIA_ROOT + 'uploads/users/' + instance.user_profile.display_name, ignore_errors=True)

# the below function was commented out
@receiver(signals.pre_save, sender=UserProductImage)
def auto_delete_file_on_change(sender: UserProductImage, instance:UserProductImage, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_image_field = UserProductImage.objects.get(pk=instance.pk)
    except UserProductImage.DoesNotExist as e:
        logger.info("New UserProductImage being installed?: {0}".format(e))
        return False

    new_file = instance.image_file
    if not old_image_field.file == new_file:
        if os.path.isfile(old_image_field.file.path):
            thumbnail.delete(old_image_field) # clear thumbs from cache
            os.remove(old_image_field.file.path)


@receiver(signals.post_save, sender=UserProductImage)
def send_email_when_image_uploaded(sender: UserProductImage, instance: UserProductImage, **kwargs):
    """
       Send email to moderators
    """
    tasks.async_task(forum_post_views.send_mod_mail, 'Image')


class Event(models.Model):
    title: models.CharField = models.CharField(max_length=50)
    text: models.CharField = models.CharField(max_length=400)
    time: models.TimeField = models.TimeField(auto_now_add=False)
    every: models.CharField = models.CharField(max_length=40, blank=True, null=True)
    event_date: models.DateField = models.DateField(auto_now_add=False, blank=True, null=True)
    repeating: models.BooleanField = models.BooleanField(default=False)
    active:models.BooleanField = models.BooleanField(default=True)
