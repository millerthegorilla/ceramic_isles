from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django_profile.models import Profile
from django.contrib.contenttypes import fields
from django.db.models.constraints import UniqueConstraint
from .soft_deletion import SoftDeletionModel

# Create your models here.


class Post(SoftDeletionModel):
    """
        post class contains category  TODO: sanitize field init parameters
    """
    text = models.TextField(max_length=2000)
    title = models.CharField(max_length=100, default='')
    slug = models.SlugField(unique=True, db_index=True, max_length=80)    # added unique and index but not tested.
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        UniqueConstraint(fields=['title', 'date_created'], name='unique_post')
        
    def get_absolute_url(self):
        return reverse_lazy('django_posts_and_comments:post_view', args=(self.id, self.slug,))

    def __str__(self):
        return f"{self.title}"

class Comment(SoftDeletionModel):
    """
        a post can have many comments
    """
    text = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, post=None, **kwargs):
        if post is not None:
            self.post = post
        super().save(**kwargs)