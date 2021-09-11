import datetime
import uuid

from django.db import models
from django.db.models.query import QuerySet
from django.contrib import admin
from django.utils import timezone
from django.conf import settings

from django_q.tasks import schedule
# The below is from https://adriennedomingus.com/blog/soft-deletion-in-django
# with djangoq added... :)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(
            SoftDeletionQuerySet,
            self).update(
            deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()
        # slack jawed duck type hack
        try:
            post_slug = self.post.slug
        except BaseException:
            post_slug = self.slug
        schedule('django_posts_and_comments.tasks.schedule_hard_delete',
                 name="sd_timeout_" + str(uuid.uuid4()),
                 schedule_type="O",
                 repeats=-1,
                 next_run=timezone.now() + settings.DELETION_TIMEOUT,
                 post_slug=post_slug,
                 deleted_at=str(self.deleted_at),
                 type=str(self),
                 id=str(self.id))

    # TODO : refactor so that a regular schedule is run once every week which hard_deletes all posts/comments
    # that are soft_deleted > than settings.DELETION_TIMEOUT ago.

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class SoftDeletionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to
        # prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()
