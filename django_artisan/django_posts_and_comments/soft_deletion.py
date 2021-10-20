import datetime
import uuid

from django.db import models
from django.db.models.query import QuerySet
from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from django.http import HttpRequest

from django_q.tasks import schedule
from typing import Any
# The below is from https://adriennedomingus.com/blog/soft-deletion-in-django
# with djangoq added... :)


class SoftDeletionQuerySet(QuerySet):
    def delete(self) -> int:
        return super(
            SoftDeletionQuerySet,
            self).update(
            deleted_at=timezone.now())

    def hard_delete(self) -> tuple[int, dict]:
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self) -> QuerySet:
        return self.filter(deleted_at=None)

    def dead(self) -> QuerySet:
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs) -> None:
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self) -> QuerySet:
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self) -> None:
        self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self) -> None:
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

    def hard_delete(self) -> None:
        super(SoftDeletionModel, self).delete()


class SoftDeletionAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to
        # prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request: HttpRequest, qs: SoftDeletionQuerySet) -> QuerySet:
        qs.hard_delete()
