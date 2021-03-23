from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe
from django.contrib import messages
from django.utils.translation import ngettext

from django_posts_and_comments.soft_deletion import SoftDeletionAdmin, SoftDeletionModel

from .models import ForumPost, ForumComment

@admin.register(ForumComment)
class ForumCommentAdmin(SoftDeletionAdmin):
    #fields = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at', 'user_profile')
    # fieldsets = [
    #     ('Moderation', {'fields': ['moderation']}),
    #     ('Active', {'fields': ['active']}),
    #     ('Author', {'fields': ['author']}),
    #     ('Text', {'fields': ['text']}),
    # ]
    list_display = ('moderation', 'active', 'post_str', 'author', 'text', 'date_created', 'deleted_at')
    list_editable = ('text', )
    list_filter = ('moderation', 'active', 'date_created', 'deleted_at', 'post', 'author')
    search_fields = ('author', 'text')

    def post_str(self, obj: ForumComment):
            link = reverse("admin:django_forum_app_forumpost_change", args=[obj.forum_post_id])
            return mark_safe(f'<a href="{link}">{escape(obj.forum_post.__str__())}</a>')

    post_str.short_description = 'ForumPost'
    post_str.admin_order_field = 'forumpost' # Make row sortable

    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        updated = queryset.update(moderation=None)
        self.message_user(request, ngettext(
                    '%d comment was approved.',
                    '%d comments were approved.',
                    updated,
                ) % updated, messages.SUCCESS)

@admin.register(ForumPost)
class ForumPostAdmin(SoftDeletionAdmin):
    list_display = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at')
    list_filter = ('moderation', 'active', 'date_created', 'deleted_at', 'author')
    search_fields = ('author', 'text', 'title')

    actions = ['approve_post']

    def approve_post(self, request, queryset):
        updated = queryset.update(moderation=None)
        self.message_user(request, ngettext(
                    '%d post was approved.',
                    '%d posts were approved.',
                    updated,
                ) % updated, messages.SUCCESS)