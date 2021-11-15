import uuid

from django.db import models
from django.dispatch import receiver
from django.template import defaultfilters
from django.contrib.contenttypes import fields
from django.db.models.constraints import UniqueConstraint
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from django.urls import reverse, reverse_lazy

from django_q.tasks import schedule

from django_messages import models as message_models
from django_profile import models as profile_models


class Post(message_models.Message):
    """
        post class contains category  TODO: sanitize field init parameters
    """
    title: models.CharField = models.CharField(max_length=100, default='')
    # added unique and index but not tested.
    user_profile: models.ForeignKey = models.ForeignKey(
        profile_models.Profile, null=True, on_delete=models.SET_NULL, related_name="posts")

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
        super().delete() ## so does this...   Model.delete sets field on model and schedules
                         ## a hard delete
    def __str__(self) -> str:
        return "Post : " + f"{self.title}"


class Comment(message_models.Message):
    """
        a post can have many comments
    """
    post_fk: models.ForeignKey = models.ForeignKey(
        Post, null=True, on_delete=models.SET_NULL, related_name="comments")
    user_profile: models.ForeignKey = models.ForeignKey(
        profile_models.Profile, null=True, on_delete=models.SET_NULL, related_name="comments")

    # def save(self, **kwargs) -> None:
    #     super().save(**kwargs)

    # class Meta:
    #     ordering = ['date_created']

    # def comment_author(self) -> str:
    #     return self.user_profile.display_name

    def __str__(self) -> str:
        # TODO check for query - fetch_related...
        return "Comment for " + f"{self.post_fk.title}"


# @receiver(post_save, sender=Comment)
# def create_comment_slug(sender: Comment, instance: Comment, created, **kwargs) -> None:
#     if created:
#         instance.title = defaultfilters.slugify(
#             instance.text[:10] + str(dateformat.format(instance.date_created, 'Y-m-d H:i:s')))
        #         instance.save()

# def scheduled_hard_delete(post_slug=None, deleted_at=None, type=None, id=None) -> None:
#     if type == 'Comment':
#         Comment.objects.get(id=id).hard_delete()
#     else:
#         Post.objects.get(id=id).hard_delete()
