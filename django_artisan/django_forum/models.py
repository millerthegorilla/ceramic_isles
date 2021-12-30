import os
import logging
from random import randint
from typing import Any, Union
from random_username import generate

from sorl import thumbnail
from safe_imagefield import models as safe_image_models

from django import urls, conf, dispatch, utils
from django.core import exceptions
from django.db import models as db_models, DEFAULT_DB_ALIAS
from django.db.models import signals, deletion
from django.contrib.auth import models as auth_models
from django.template import defaultfilters

from django_profile import models as profile_models
from django_messages import models as messages_models

logger = logging.getLogger('django_artisan')

# START PROFILE
# helper functions
def default_display_name() -> str:
    return generate.generate_username()[0]

## TODO see if Union below is necessary...
def user_directory_path_avatar(instance: Union['Post','Comment'], filename: str) -> str:
    return 'uploads/users/{0}/avatar/{1}'.format(
        instance.user_profile.display_name, filename)

def default_avatar(num: int) -> str:
    return 'default_avatars/default_avatar_{0}.jpg'.format(num)
# end helper functions


# START AVATAR
class Avatar(db_models.Model):
    image_file = safe_image_models.SafeImageField(upload_to=user_directory_path_avatar)


@dispatch.receiver(signals.pre_save, sender=Avatar)
def auto_delete_file_on_change(sender: Avatar, instance: Avatar, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_avatar = Avatar.objects.get(pk=instance.pk)
    except Avatar.DoesNotExist as e:
        logger.warn("unable to get old avatar file : {0}".format(e))
        return False

    if 'default_avatars' not in old_avatar.image_file.path:
        new_file = instance.image_file
        if not old_avatar.image_file == new_file:
            if os.path.isfile(old_avatar.image_file.path):
                try:
                    thumbnail.delete(old_avatar.image_file)
                except exceptions.ObjectDoesNotExist as e:
                    logger.error(
                        "Error, avatar does not exist : {0}".format(e))
# END AVATAR


class ForumProfile(profile_models.Profile):
    address_line_1: db_models.CharField = db_models.CharField(
        'address line 1', max_length=30, blank=True, default='')
    address_line_2: db_models.CharField = db_models.CharField(
        'address line 2', max_length=30, blank=True, default='')
    parish: db_models.CharField = db_models.CharField('parish', max_length=30, blank=True, default='')
    postcode: db_models.CharField = db_models.CharField(
        'postcode', max_length=6, blank=True, default='')
    avatar: db_models.OneToOneField = db_models.OneToOneField(
        Avatar, on_delete=db_models.CASCADE, related_name='user_profile')
    rules_agreed: db_models.BooleanField = db_models.BooleanField(default='False')
    display_name: db_models.CharField = db_models.CharField(
        max_length=37, blank=True, unique=True, default=default_display_name)

    def username(self) -> str:
        return self.profile_user.username

    class Meta:
        try:
            abstract = conf.settings.ABSTRACTFORUMPROFILE
        except AttributeError:
            abstract = False

    # def delete(self, *args, **kwargs):
    #     breakpoint()
    #     super.delete(*args, **kwargs)
    #     self.avatar.delete()
"""
    disconnect dummy profile
"""
signals.post_save.disconnect(profile_models.create_user_profile, sender=auth_models.User)
#signals.post_save.disconnect(profile_models.save_user_profile, sender=auth_models.User)
"""
    Custom signals to create and update user profile
"""


@dispatch.receiver(signals.post_save, sender=auth_models.User)
def create_user_forum_profile(sender: auth_models.User, instance: auth_models.User, created: bool = False, **kwargs) -> None:
    if created:
        ForumProfile.objects.create(
            profile_user=instance,
            avatar=Avatar.objects.create(
                image_file=default_avatar(
                    randint(
                        1,
                        4))))
    try:
        instance.profile.save()
    except (exceptions.ObjectDoesNotExist, exceptions.FieldError) as e:
        logger.error("Error saving forum profile : {0}".format(e))

# @dispatch.receiver(signals.post_save, sender=auth_models.User)
# def save_user_forum_profile(sender: auth_models.User, instance: auth_models.User, **kwargs) -> None:
#     try:
#         instance.profile.save()
#     except (exceptions.ObjectDoesNotExist, exceptions.FieldError) as e:
#         logger.error("Error saving forum profile : {0}".format(e))

signals.post_save.connect(create_user_forum_profile, sender=auth_models.User)
#signals.post_save.connect(save_user_forum_profile, sender=auth_models.User)


@dispatch.receiver(signals.pre_delete, sender=ForumProfile)
def auto_delete_avatar_on_delete(sender: ForumProfile, instance: ForumProfile, **kwargs) -> None:
    """
    Deletes Avatar from filesystem
    when corresponding `ForumProfile` object is deleted.
    """
    fp = instance.avatar.image_file.path
    fd = os.path.dirname(fp)
    if instance.avatar.image_file and 'default_avatars' not in instance.avatar.image_file.path:
        if os.path.isfile(fp):
            try:
                thumbnail.delete(instance.avatar.image_file)
                instance.avatar.delete()
                if len(os.listdir(fd)) == 0:
                    os.rmdir(fd)
                fdu1 = conf.settings.MEDIA_ROOT + \
                    'uploads/users/' + \
                    instance.display_name
                if os.path.isdir(fdu1):
                    if len(os.listdir(fdu1)) == 0:
                        os.rmdir(fdu1)
            except exceptions.ObjectDoesNotExist as e:
                logger.error("unable to delete avatar : {0}".format(e))

# START POST AND COMMENTS

## TODO Post and Comment should probably have common superclass somewhere.

class Post(messages_models.Message):
    title: db_models.CharField = db_models.CharField(max_length=100, default='')
    pinned: db_models.SmallIntegerField = db_models.SmallIntegerField(default=0)
    subscribed_users: db_models.ManyToManyField = db_models.ManyToManyField(
        auth_models.User, blank=True, related_name="subscribed_posts")
    commenting_locked: db_models.BooleanField = db_models.BooleanField(default=False)

    class Meta(messages_models.Message.Meta):
        ordering = ['-created_at']
        permissions = [('approve_post', 'Approve Post')]
        messages_models.Message._meta.get_field('text').max_length = 3000
        try:
            abstract = conf.settings.ABSTRACTPOST
        except AttributeError:
            abstract = False

    def get_absolute_url(self, a_name:str = 'django_forum') -> str:
        return urls.reverse_lazy(
            a_name + ':post_view', 
            args=[self.id, self.slug]) # type: ignore

    def get_author_name(self) -> str:
        return self.author.profile.display_name

    def __str__(self) -> str:
        return f"{self.author.profile.display_name}"

# if django_forum.models.Post is abstract then the below needs to know what Post model
# is being used.  TODO  make sure that docs indicate that POST_MODEL must be set if
# ABSTRACTPOST is True.
import importlib
try:
    post_model = eval('conf.settings.POST_MODEL')
except AttributeError:
    post_model = Post
class Comment(messages_models.Message):
    # author: models.CharField = models.CharField(default='', max_length=40)
    post_fk: db_models.ForeignKey = db_models.ForeignKey(
        post_model, on_delete=db_models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['created_at']
        permissions = [('approve_comment', 'Approve Comment')]
        try:
            abstract = conf.settings.ABSTRACTCOMMENT
        except AttributeError:
            abstract = False

    def get_absolute_url(self) -> str:
        return self.post_fk.get_absolute_url() + '#' + self.slug

    def get_category_display(self) -> str:
        return 'Comment'

    def get_author_name(self) -> str:
        return self.author.profile.display_name

# @dispatch.receiver(post_save, sender=Comment)
# def save_author_on_comment_creation(sender: Comment, instance: Comment, created, **kwargs) -> None:
#     if created:
#         instance.author = instance.comment_author()
#         instance.title = slugify(
#             instance.text[:10] + str(dateformat.format(instance.created_at, 'Y-m-d H:i:s')))
#         instance.save()

# END POSTS AND COMMENTS
