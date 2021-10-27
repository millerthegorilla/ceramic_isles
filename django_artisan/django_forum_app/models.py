import os
import logging
from random import randint
from typing import Any, Union

from django.db.models import Max
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_init, post_save, pre_save, post_delete, pre_delete
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils.translation import gettext_lazy as _
from django.utils import dateformat
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django_profile.models import Profile
from django_profile.models import create_user_profile, save_user_profile
from django_posts_and_comments.models import Post, Comment
from safe_imagefield.models import SafeImageField
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail import delete

_: Any

logger = logging.getLogger('django')

# START PROFILE
# helper functions

## TODO see if Union below is necessary...
def user_directory_path_avatar(instance: Union['ForumPost','ForumComment'], filename: str) -> str:
    return 'uploads/users/{0}/avatar/{1}'.format(
        instance.user_profile.display_name, filename)


def default_avatar(num: int) -> str:
    return 'default_avatars/default_avatar_{0}.jpg'.format(num)
# end helper functions


# START AVATARS

class Avatar(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path_avatar)


@receiver(pre_save, sender=Avatar)
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
                    delete(old_avatar.image_file)
                except ObjectDoesNotExist as e:
                    logger.error(
                        "Error, avatar does not exist : {0}".format(e))

# END AVATARS


class ForumProfile(Profile):
    address_line_1 = models.CharField(
        'address line 1', max_length=30, blank=True, default='')
    address_line_2 = models.CharField(
        'address line 2', max_length=30, blank=True, default='')
    parish = models.CharField('parish', max_length=30, blank=True, default='')
    postcode = models.CharField(
        'postcode', max_length=6, blank=True, default='')
    avatar = models.OneToOneField(
        Avatar, on_delete=models.CASCADE, related_name='user_profile')
    rules_agreed = models.BooleanField(default='False')

    def username(self) -> str:
        return self.profile_user.username

    # def delete(self, *args, **kwargs):
    #     breakpoint()
    #     super.delete(*args, **kwargs)
    #     self.avatar.delete()
"""
    disconnect dummy profile
"""
post_save.disconnect(create_user_profile, sender=User)
post_save.disconnect(save_user_profile, sender=User)
"""
    Custom signals to create and update user profile
"""


@receiver(post_save, sender=User)
def create_user_forum_profile(sender: User, instance: User, created: bool, **kwargs) -> None:
    if created:
        ForumProfile.objects.create(
            profile_user=instance,
            avatar=Avatar.objects.create(
                image_file=default_avatar(
                    randint(
                        1,
                        4))))
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_forum_profile(sender: User, instance: User, **kwargs) -> None:
    try:
        instance.profile.save()
    except (ObjectDoesNotExist, FieldError) as e:
        logger.error("Error saving forum profile : {0}".format(e))


@receiver(pre_delete, sender=ForumProfile)
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
                delete(instance.avatar.image_file)
                instance.avatar.delete()
                if len(os.listdir(fd)) == 0:
                    os.rmdir(fd)
                fdu1 = settings.MEDIA_ROOT + \
                    'uploads/users/' + \
                    instance.display_name
                if os.path.isdir(fdu1):
                    if len(os.listdir(fdu1)) == 0:
                        os.rmdir(fdu1)
            except ObjectDoesNotExist as e:
                logger.error("unable to delete avatar : {0}".format(e))

# START POST AND COMMENTS

## TODO Post and Comment should probably have common superclass somewhere.

class ForumPost(Post):
    author: models.CharField = models.CharField(default='', max_length=40)
    active: models.BooleanField = models.BooleanField(default=True)
    moderation: models.DateField = models.DateField(null=True, default=None, blank=True)
    pinned:models.SmallIntegerField = models.SmallIntegerField(default=0)
    subscribed_users: models.ManyToManyField = models.ManyToManyField(
        User, blank=True, related_name="subscribed_posts")

    class Meta:
        ordering = ['-date_created']
        permissions = [('approve_post', 'Approve Post')]

    category = models.CharField(
        max_length=2,
        choices=settings.CATEGORY.choices,
        default=settings.CATEGORY.GENERAL,
    )

    location = models.CharField(
        max_length=2,
        choices=settings.LOCATION.choices,
        default=settings.LOCATION.ANY_ISLE,
    )

    def get_absolute_url(self) -> str:
        return reverse_lazy(
            'django_forum_app:post_view', args=(
                self.id, self.slug,))

    def __str__(self) -> str:
        return f"Post by {self.author}"

    def category_label(self) -> str:
        return settings.CATEGORY(self.category).label

    def location_label(self) -> str:
        return settings.LOCATION(self.location).label


@receiver(post_save, sender=ForumPost)
def save_author_on_post_creation(sender: ForumPost, instance: ForumPost, created, **kwargs) -> None:
    if created:
        instance.author = instance.post_author()
        instance.save()


class ForumComment(Comment):
    author = models.CharField(default='', max_length=40)
    forum_post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="forum_comments")
    active = models.BooleanField(default='True')
    moderation = models.DateField(null=True, default=None, blank=True)
    title = models.SlugField()

    class Meta:
        ordering = ['date_created']
        permissions = [('approve_comment', 'Approve Comment')]

    def save(self, **kwargs) -> None:
        super().save(post=self.forum_post, **kwargs)

    def get_absolute_url(self) -> str:
        return self.forum_post.get_absolute_url() + '#' + self.title

    def get_category_display(self) -> str:
        return 'Comment'


@receiver(post_save, sender=ForumComment)
def save_author_on_comment_creation(sender: ForumComment, instance: ForumComment, created, **kwargs) -> None:
    if created:
        instance.author = instance.comment_author()
        instance.title = slugify(
            instance.text[:10] + str(dateformat.format(instance.date_created, 'Y-m-d H:i:s')))
        instance.save()

# END POSTS AND COMMENTS
