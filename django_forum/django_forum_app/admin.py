from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from django_posts_and_comments.soft_deletion import SoftDeletionAdmin, SoftDeletionModel

from .models import ForumPost, ForumComment, ForumProfileImage


@admin.register(ForumComment)
class ForumCommentAdmin(SoftDeletionAdmin):
    list_display = ('moderation', 'active', 'post_str', 'author', 'text', 'date_created', 'deleted_at')
    list_filter = ('moderation', 'active', 'date_created', 'deleted_at', 'post', 'author')
    search_fields = ('author', 'text')

    def post_str(self, obj: ForumComment):
            link = reverse("admin:django_forum_app_forumpost_change", args=[obj.forum_post_id])
            return mark_safe(f'<a href="{link}">{escape(obj.forum_post.__str__())}</a>')

    post_str.short_description = 'ForumPost'
    post_str.admin_order_field = 'forumpost' # Make row sortable
    
    # def link_to_post(self, obj):
    #     link=reverse("admin:django_forum_app_forumpost_change", args=[obj.forum_post.id]) #model name has to be lowercase
    #     return format_html('<a href="%s">%s</a>' % (link, obj.forum_post.title))

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