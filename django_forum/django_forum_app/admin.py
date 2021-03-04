from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from django_posts_and_comments.soft_deletion import SoftDeletionAdmin, SoftDeletionModel

from .models import ForumPost, ForumComment, ForumProfileImage, Event


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

@admin.register(ForumPost)
class ForumPostAdmin(SoftDeletionAdmin):
    list_display = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at')
    list_filter = ('moderation', 'active', 'date_created', 'deleted_at', 'author')
    search_fields = ('author', 'text', 'title')


@admin.register(ForumProfileImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('active', 'image_file', 'image_shop_link', 'image_title', 'image_text', 'image_shop_link_title')
    list_filter = ('active', 'image_file', 'image_title')
    search_fields = ('image_text', 'image_title', 'image_shop_link')
    actions = ['approve_image']

    def approve_image(self, request, queryset):
        queryset.update(active=True)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('active', 'title', 'text', 'date', 'repeating')
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request, queryset):
        queryset.update(active=True)

    def disapprove_event(self, request, queryset):
        queryset.update(active=False)