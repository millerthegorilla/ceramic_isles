import os
import uuid
from random import randint

from django.db.models import Max
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_init, post_save, pre_save, post_delete
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.conf import settings

from django_profile.models import Profile
from django_profile.models import create_user_profile, save_user_profile
from django_posts_and_comments.models import Post, Comment
from safe_filefield.models import SafeImageField
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail import delete
### START PROFILE
### helper functions

def user_directory_path(instance, filename):
    return 'uploads/users/{0}/{1}'.format(instance.user_profile.profile_user, filename)

def user_directory_path_avatar(instance, filename):
    return 'uploads/users/{0}/avatar/{1}'.format(instance.user_profile.profile_user, filename)

def default_avatar(num):
    return 'default_avatars/default_avatar_{0}.jpg'.format(num)
### end helper functions


### START AVATARS

class Avatar(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path_avatar)
    
### END AVATARS    image_file = models.ImageField(upload_to=user_directory_path, null=True)


class ForumProfile(Profile):
    bio = models.TextField(max_length=500, blank=True, default='')
    address_line_1 = models.CharField(max_length=30, blank=True, default='')
    address_line_2 = models.CharField(max_length=30, blank=True, default='')
    parish = models.CharField(max_length=30, blank=True, default='')
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')
    shop_web_address = models.CharField(max_length=50, blank=True, default='')
    outlets = models.CharField(max_length=400, blank=True, default='')
    avatar = models.OneToOneField(Avatar, on_delete=models.CASCADE, 
                                          related_name='user_profile')

"""
    disconnect dummy profile
"""
post_save.disconnect(create_user_profile, sender=User)
post_save.disconnect(save_user_profile, sender=User)
"""
    Custom signals to create and update user profile
"""
@receiver(post_save, sender=User)
def create_user_forum_profile(sender, instance, created, **kwargs):
    if created:
        ForumProfile.objects.create(profile_user=instance, 
                                    avatar=Avatar.objects.create(
                                        image_file=default_avatar(randint(1,4))))
        instance.profile.user_slug = slugify(instance.username)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_forum_profile(sender, instance, **kwargs):
    try:
        instance.profile.forumprofile.save()
    except (ObjectDoesNotExist, FieldError):
        pass
        ## TODO: log error to log file.


###  START PROFILEIMAGE

# TODO: validate image_shop_link properly 
# TODO: set a default of 
class ForumProfileImage(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path)
    image_text = models.CharField(max_length=400, default='')
    image_title = models.CharField(max_length=30, default='')
    image_shop_link = models.CharField(max_length=50, default='#')
    image_shop_link_title = models.CharField(max_length=30, default='')
    active = models.BooleanField(default=False)
    user_profile = models.ForeignKey(ForumProfile, on_delete=models.CASCADE, related_name="forum_images")
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


@receiver(post_delete, sender=ForumProfileImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image_file:
        delete(instance.image_file)
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)

@receiver(pre_save, sender=ForumProfileImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image_field = ForumProfileImage.objects.get(pk=instance.pk)
    except ForumProfileImage.DoesNotExist:
        return False

    new_file = instance.image_file
    if not old_image_field.file == new_file:
        if os.path.isfile(old_image_field.file.path):
            delete(old_image_field) # clear thumbs from cache
            os.remove(old_image_field.file.path)
### END PROFILEIMAGE

### END PROFILE

### START POST AND COMMENTS
class ForumPost(Post):
    user_profile = models.ForeignKey(ForumProfile, on_delete=models.CASCADE, related_name="posts")
    author = models.CharField(default='', max_length=40)
    active = models.BooleanField(default='True')
    moderation = models.BooleanField(default='False')
    
    class Meta:
        ordering = ['-date_created']
    
    def post_author(self):
        if self.user_profile is not None:
            return self.user_profile.profile_user.username


    class Category(models.TextChoices):
        EVENT = 'EV', _('Event')
        QUESTION = 'QN', _('Question')
        GENERAL = 'GL', _('General')
        PICTURES = 'PS', _('Pictures')
        FORSALE = 'FS', _('For Sale')

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    def get_absolute_url(self):
        return reverse_lazy('django_forum_app:post_view', args=(self.id, self.slug,))

    def __str__(self):
        return f"Post by {self.author}"

@receiver(post_save, sender=ForumPost)
def save_author_on_post_creation(sender, instance, created, **kwargs):
    if created:
        instance.author = instance.post_author()
        instance.save()

class ForumComment(Comment):
    user_profile = models.ForeignKey(ForumProfile, on_delete=models.CASCADE, related_name="forum_comments")
    author = models.CharField(default='', max_length=40)
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="forum_comments")
    active = models.BooleanField(default='True')
    moderation = models.BooleanField(default='False')

    def save(self, **kwargs):
        super().save(post=self.forum_post, **kwargs)

    class Meta:
        ordering = ['date_created']
        
    def comment_author(self):
        return self.user_profile.profile_user.username

@receiver(post_save, sender=ForumComment)
def save_author_on_comment_creation(sender, instance, created, **kwargs):
    if created:
        instance.author = instance.comment_author()
        instance.save()
        
### END POSTS AND COMMENTS
