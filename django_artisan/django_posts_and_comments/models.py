import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django_profile.models import Profile
from django.contrib.contenttypes import fields
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from django.conf import settings

from django_q.tasks import schedule

from .soft_deletion import SoftDeletionModel
from typing import Any


class Post(SoftDeletionModel):
    """
        post class contains category  TODO: sanitize field init parameters
    """
    text: models.TextField = models.TextField(max_length=2000)
    title: models.CharField = models.CharField(max_length=100, default='')
    # added unique and index but not tested.
    slug: models.SlugField = models.SlugField(unique=True, db_index=True, max_length=80)
    date_created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user_profile: models.ForeignKey = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="posts")

    class Meta:
        UniqueConstraint(fields=['title', 'date_created'], name='unique_post')

    def post_author(self) -> str:
        return self.user_profile.display_name

    def get_absolute_url(self) -> str:
        return reverse_lazy(
            'django_posts_and_comments:post_view', args=(
                self.id, self.slug,))

    def delete(self) -> None:
        for comment in self.comments.all():
            comment.delete()   ## -> calls softdeletionModel.delete
        super().delete() ## so does this...   SoftDeletionModel.delete sets field on model and schedules
                         ## a hard delete
    def __str__(self) -> str:
        return "Post : " + f"{self.title}"


class Comment(SoftDeletionModel):
    """
        a post can have many comments
    """
    text: models.TextField = models.TextField(max_length=500)
    post: models.ForeignKey = models.ForeignKey(
        Post, null=True, on_delete=models.SET_NULL, related_name="comments")
    date_created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user_profile: models.ForeignKey = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="comments")

    # def save(self, **kwargs) -> None:
    #     super().save(**kwargs)

    def comment_author(self) -> str:
        return self.user_profile.display_name

    def __str__(self) -> str:
        # TODO check for query - fetch_related...
        return "Comment for " + f"{self.post.title}"

# def scheduled_hard_delete(post_slug=None, deleted_at=None, type=None, id=None) -> None:
#     if type == 'Comment':
#         Comment.objects.get(id=id).hard_delete()
#     else:
#         Post.objects.get(id=id).hard_delete()
