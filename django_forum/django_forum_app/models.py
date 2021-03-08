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
from django.utils import dateformat
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.conf import settings

from django_profile.models import Profile
from django_profile.models import create_user_profile, save_user_profile
from django_posts_and_comments.models import Post, Comment
from safe_imagefield.models import SafeImageField
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail import delete
### START PROFILE
### helper functions
def user_directory_path_avatar(instance, filename):
    return 'uploads/users/{0}/avatar/{1}'.format(instance.user_profile.display_name, filename)

def default_avatar(num):
    return 'default_avatars/default_avatar_{0}.jpg'.format(num)
### end helper functions


### START AVATARS

class Avatar(models.Model):
    image_file = models.ImageField(upload_to=user_directory_path_avatar)
    
### END AVATARS 


class ForumProfile(Profile):
    bio = models.TextField('biographical information, max 500 chars', 
                            max_length=500, 
                            blank=True, 
                            default='', 
                            help_text="This is the biographical information that will be presented on your personal page")
    address_line_1 = models.CharField('address line 1', max_length=30, blank=True, default='')
    address_line_2 = models.CharField('address line 2', max_length=30, blank=True, default='')
    parish = models.CharField('parish', max_length=30, blank=True, default='')
    postcode = models.CharField('postcode', max_length=6, blank=True, default='')
    avatar = models.OneToOneField(Avatar, on_delete=models.CASCADE, related_name='user_profile')
    rules_agreed = models.BooleanField(default='False')
    
    def username(self):
        return self.profile_user.username
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
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_forum_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except (ObjectDoesNotExist, FieldError):
        pass
        ## TODO: log error to log file.

### START POST AND COMMENTS
class ForumPost(Post):
    author = models.CharField(default='', max_length=40)
    active = models.BooleanField(default=True)
    moderation = models.DateField(null=True, default=None, blank=True)
    
    class Meta:
        ordering = ['-date_created']

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
    author = models.CharField(default='', max_length=40)
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="forum_comments")
    active = models.BooleanField(default='True')
    moderation = models.DateField(null=True, default=None, blank=True)
    title = models.SlugField()

    def save(self, **kwargs):
        super().save(post=self.forum_post, **kwargs)

    class Meta:
        ordering = ['date_created']

    def get_absolute_url(self):
        return self.forum_post.get_absolute_url() + '#' + self.title

    def get_category_display(self):
        return 'Comment'

@receiver(post_save, sender=ForumComment)
def save_author_on_comment_creation(sender, instance, created, **kwargs):
    if created:
        instance.author = instance.comment_author()
        instance.title = slugify(instance.text[:10] + str(dateformat.format(instance.date_created, 'Y-m-d H:i:s')))
        instance.save()
        
### END POSTS AND COMMENTS