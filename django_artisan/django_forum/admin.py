import logging

from django import conf, http, urls, utils
from django.contrib import admin, messages
from django.db import models as db_models

from django_messages import soft_deletion

from . import models as forum_models

logger = logging.getLogger('django_artisan')
try:
    abs_comment = conf.settings.ABSTRACTCOMMENT
except AttributeError:
    abs_comment = False
if not abs_comment:
    @admin.register(forum_models.Comment)
    class Comment(soft_deletion.Admin):
        #fields = ('moderation', 'active', 'author', 'title', 'text', 'created_at', 'deleted_at', 'user_profile')
        # fieldsets = [
        #     ('Moderation', {'fields': ['moderation']}),
        #     ('Active', {'fields': ['active']}),
        #     ('Author', {'fields': ['author']}),
        #     ('Text', {'fields': ['text']}),
        # ]
        list_display = ('moderation_date', 'active', 'post_str',
                        'author', 'text', 'created_at', 'deleted_at')
        list_editable = ('text', )
        list_filter = ('moderation_date', 'active', 'created_at',
                       'post_fk', 'author', 'deleted_at')
        search_fields = ('author', 'text')

        def post_str(self, obj: forum_models.Comment) -> str:
            link = urls.reverse("admin:django_forum_forumpost_change",
                           args=[obj.post.id])
            return utils.safestring.mark_safe(
                f'<a href="{link}">{utils.html.escape(obj.post.__str__())}</a>')

        post_str.short_description = 'Post' # type: ignore
        # make row sortable
        post_str.admin_order_field = 'post'  # type: ignore

        actions = ['approve_comment']

        def approve_comment(self, request: http.HttpRequest, queryset: db_models.QuerySet):
            updated = queryset.update(moderation_date=None)

            self.message_user(request,
                              utils.translation.ngettext(
                                        '%d comment was approved.',
                                        '%d comments were approved.',
                                        updated,
                                  ) % updated, 
                              messages.SUCCESS)

try:
    abs_post = conf.settings.ABSTRACTPOST
except AttributeError:
    abs_post = False
if not abs_post:
    @admin.register(forum_models.Post)
    class Post(soft_deletion.Admin):
        list_display = ('commenting_locked', 'pinned', 'moderation_date', 'active', 'author',
                        'title', 'text', 'created_at', 'deleted_at')
        list_filter = ('commenting_locked', 'pinned', 'moderation_date', 'active',
                       'created_at', 'author', 'deleted_at')
        search_fields = ('author', 'text', 'title')

        actions = ['approve_post', 'lock_commenting', 'unlock_commenting', 'unpin_post']

        def approve_post(self, request: http.HttpRequest,
                               queryset: db_models.QuerySet) -> None:
            idx = 0
            for q in queryset:
                q.moderation_date = None
                try:
                    q.save(update_fields=['moderation_date'])
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

        def lock_commenting(self, request: http.HttpRequest, 
                                queryset: db_models.QuerySet) -> None:
            idx = 0
            for q in queryset:
                q.commenting_locked = True
                try:
                    q.save(update_fields=['commenting_locked'])
                    idx += 1
                except Exception as e:
                    logger.error("Error locking comments : {0}".format(e))
            
            self.message_user(request,
                              utils.translation.ngettext(
                                    'commenting on %d post was locked.',
                                    'commenting on %d posts was locked.',
                                    idx,
                              ) % idx, 
                              messages.SUCCESS)

        def unlock_commenting(self, request: http.HttpRequest, 
                                  queryset: db_models.QuerySet) -> None:
            idx = 0
            for q in queryset:
                q.commenting_locked = False
                try:
                    q.save(update_fields=['commenting_locked'])
                    idx += 1
                except Exception as e:
                    logger.error("Error unlocking comments : {0}".format(e))
            
            self.message_user(request,
                              utils.translation.ngettext(
                                    'commenting on %d post was unlocked.',
                                    'commenting on %d posts was unlocked.',
                                    idx,
                              ) % idx, 
                              messages.SUCCESS)

        def unpin_post(self, request: http.HttpRequest, 
                             queryset: db_models.QuerySet) -> None:
            idx = 0
            for q in queryset:
                q.pinned = 0
                try:
                    q.save(update_fields=['pinned'])
                    idx += 1
                except Exception as e:
                    logger.error("Error unpinning posts: {0}".format(e))
            
            self.message_user(request,
                              utils.translation.ngettext(
                                    '%d post was unpinned.',
                                    '%d posts were unpinned.',
                                    idx,
                              ) % idx, 
                              messages.SUCCESS)

try:
    abs_forum_profile = conf.settings.ABSTRACTFORUMPROFILE
except AttributeError:
    abs_forum_profile = False
if not abs_forum_profile:
    if not conf.settings.ABSTRACTPROFILE:
        admin.site.unregister(Profile)
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
