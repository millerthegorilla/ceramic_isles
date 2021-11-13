import logging

from django.contrib import admin
from django import urls, utils, http
from django.contrib import messages
from django.conf import settings
from django.db import models as db_models

from django_messages import soft_deletion

from . import models as forum_models

logger = logging.getLogger('django_artisan')


@admin.register(forum_models.ForumComment)
class ForumComment(soft_deletion.Admin):
    #fields = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at', 'user_profile')
    # fieldsets = [
    #     ('Moderation', {'fields': ['moderation']}),
    #     ('Active', {'fields': ['active']}),
    #     ('Author', {'fields': ['author']}),
    #     ('Text', {'fields': ['text']}),
    # ]
    list_display = ('moderation', 'active', 'post_str',
                    'author', 'text', 'date_created', 'deleted_at')
    list_editable = ('text', )
    list_filter = ('moderation', 'active', 'date_created',
                   'post_fk', 'author', 'deleted_at')
    search_fields = ('author', 'text')

    def post_str(self, obj: forum_models.ForumComment) -> str:
        link = urls.reverse("admin:django_forum_forumpost_change",
                       args=[obj.forum_post.id])
        return utils.safestring.mark_safe(
            f'<a href="{link}">{utils.html.escape(obj.forum_post.__str__())}</a>')

    post_str.short_description = 'ForumPost' # type: ignore
    # make row sortable
    post_str.admin_order_field = 'forumpost'  # type: ignore

    actions = ['approve_comment']

    def approve_comment(self, request: http.HttpRequest, queryset: db_models.QuerySet):
        # idx = 0
        # for q in queryset:
        #     q.moderation = None
        #     try:
        #         q.save(update_fields=['moderation'])
        #         idx += 1
        #     except Exception as e:
        #         logger.error("Error approving moderation : {0}".format(e))
        updated = queryset.update(moderation=None)

        self.message_user(request,
                          utils.translation.ngettext(
                                    '%d comment was approved.',
                                    '%d comments were approved.',
                                    updated,
                              ) % updated, 
                          messages.SUCCESS)


@admin.register(forum_models.ForumPost)
class ForumPost(soft_deletion.Admin):
    list_display = ('pinned', 'moderation', 'active', 'author',
                    'title', 'text', 'date_created', 'deleted_at')
    list_filter = ('pinned', 'moderation', 'active',
                   'date_created', 'author', 'deleted_at')
    search_fields = ('author', 'text', 'title')

    actions = ['approve_post']

    def approve_post(self, request: http.HttpRequest, queryset: db_models.QuerySet):
        idx = 0
        for q in queryset:
            q.moderation = None
            try:
                q.save(update_fields=['moderation'])
                idx += 1
            except Exception as e:
                logger.error("Error approving moderation : {0}".format(e))
        
        self.message_user(request,
                          utils.translation.ngettext(
                                '%d post was approved.',
                                '%d posts were approved.',
                                idx,
                          ) % idx, 
                          messages.SUCCESS)

    # def pin_post(self, request: HttpRequest queryset):
    #     self.message_user(request: HttpRequest ngettext(
    #                 '%d post was approved.',
    #                 '%d posts were approved.',
    #                 updated,
    #             ) % updated, messages.SUCCESS)


# admin.site.unregister(Profile)

# Register your models here.
@admin.register(forum_models.ForumProfile)
class ForumProfile(admin.ModelAdmin):
    list_display = [
        'display_name',
        'address_line_1',
        'address_line_2',
        'parish',
        'postcode',
        'avatar',
        'rules_agreed']
    list_filter = ['display_name', 'parish', 'rules_agreed']
    search_fields = ['display_name', 'address_line_1']

    def get_queryset(self, request: http.HttpRequest) -> db_models.QuerySet:
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)
