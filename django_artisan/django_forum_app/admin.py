from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.utils.translation import ngettext
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import QuerySet
from django.http import HttpRequest

from django_posts_and_comments.soft_deletion import SoftDeletionAdmin, SoftDeletionModel
from django_profile.models import Profile

from .models import ForumPost, ForumComment, ForumProfile


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):  # SoftDeletionAdmin):
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
                   'post', 'author', 'deleted_at')
    search_fields = ('author', 'text')

    def post_str(self, obj: ForumComment) -> str:
        link = reverse("admin:django_forum_app_forumpost_change",
                       args=[obj.forum_post_id])
        return mark_safe(
            f'<a href="{link}">{escape(obj.forum_post.__str__())}</a>')

    post_str.short_description = 'ForumPost'
    post_str.admin_order_field = 'forumpost'  # Make row sortable

    actions = ['approve_comment']

    def approve_comment(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(moderation=None)
        self.message_user(request,
                          ngettext(
                                '%d comment was approved.',
                                '%d comments were approved.',
                                updated,
                          ) % updated, 
                          messages.SUCCESS)


@admin.register(ForumPost)
class ForumPostAdmin(SoftDeletionAdmin):
    list_display = ('pinned', 'moderation', 'active', 'author',
                    'title', 'text', 'date_created', 'deleted_at')
    list_filter = ('pinned', 'moderation', 'active',
                   'date_created', 'author', 'deleted_at')
    search_fields = ('author', 'text', 'title')

    actions = ['approve_post']

    def approve_post(self, request: HttpRequest, queryset: QuerySet):
        updated = queryset.update(moderation=None)
        self.message_user(request,
                          ngettext(
                            '%d post was approved.',
                            '%d posts were approved.',
                            updated,
                          ) % updated,
                          messages.SUCCESS)

    # def pin_post(self, request: HttpRequest queryset):
    #     self.message_user(request: HttpRequest ngettext(
    #                 '%d post was approved.',
    #                 '%d posts were approved.',
    #                 updated,
    #             ) % updated, messages.SUCCESS)


# admin.site.unregister(Profile)

# Register your models here.
@admin.register(ForumProfile)
class ForumProfileAdmin(admin.ModelAdmin):
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

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)
