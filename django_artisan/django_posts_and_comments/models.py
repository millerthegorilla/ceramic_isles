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


class Post(SoftDeletionModel):
    """
        post class contains category  TODO: sanitize field init parameters
    """
    text = models.TextField(max_length=2000)
    title = models.CharField(max_length=100, default='')
    # added unique and index but not tested.
    slug = models.SlugField(unique=True, db_index=True, max_length=80)
    date_created = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="posts")

    class Meta:
        UniqueConstraint(fields=['title', 'date_created'], name='unique_post')

    def post_author(self):
        return self.user_profile.display_name

    def get_absolute_url(self):
        return reverse_lazy(
            'django_posts_and_comments:post_view', args=(
                self.id, self.slug,))

    def delete(self):
        super().delete()
        for comment in self.comments.all():
            comment.delete()
        # schedule(schedule_hard_delete, name="sd_timeout_" + str(uuid.uuid4()),
        #                                schedule_type="O",
        #                                repeats=-1,
        #                                next_run=timezone.now() + settings.DELETION_TIMEOUT,
        #                                kwargs={'post_slug': self.post.slug,
        #                                        'deleted_at': str(self.deleted_at),
        #                                        'type': 'Post',
        #                                        'id': self.id })

    def __str__(self):
        return "Post : " + f"{self.title}"


class Comment(SoftDeletionModel):
    """
        a post can have many comments
    """
    text = models.TextField(max_length=500)
    post = models.ForeignKey(
        Post, null=True, on_delete=models.SET_NULL, related_name="comments")
    date_created = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(
        Profile, null=True, on_delete=models.SET_NULL, related_name="comments")

    def save(self, post=None, **kwargs):
        if post is not None:
            self.post = post
        super().save(**kwargs)

    def comment_author(self):
        return self.user_profile.display_name

    def __str__(self):
        # TODO check for query - fetch_related...
        return "Comment for " + f"{self.post.title}"

    # def delete(self):
    #     super().delete()
    #     schedule(schedule_hard_delete, name="sd_timeout_" + str(uuid.uuid4()),
    #                                    schedule_type="O",
    #                                    repeats=-1,
    #                                    next_run=timezone.now() + settings.DELETION_TIMEOUT,
    #                                    kwargs={'post_slug': self.post.slug,
    #                                            'deleted_at': str(self.deleted_at),
    #                                            'type': 'Comment',
    #                                            'id': self.id })


def schedule_hard_delete(post_slug=None, deleted_at=None, type=None, id=None):
    if type == 'Comment':
        Comment.objects.get(id=id).hard_delete()
    else:
        Post.objects.get(id=id).hard_delete()
