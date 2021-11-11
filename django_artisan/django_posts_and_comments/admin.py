from django.contrib import admin
# from django.urls import reverse

# from .models import Comment


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):  # Admin):
#     #fields = ('moderation', 'active', 'author', 'title', 'text', 'date_created', 'deleted_at', 'user_profile')
#     # fieldsets = [
#     #     ('Moderation', {'fields': ['moderation']}),
#     #     ('Active', {'fields': ['active']}),
#     #     ('Author', {'fields': ['author']}),
#     #     ('Text', {'fields': ['text']}),
#     # ]
#     list_display = ('author', 'text', 'date_created') # 'deleted_at')
#     list_editable = ('text', )
#     list_filter = ('date_created',
#                    'post', 'author') # 'deleted_at')
#     search_fields = ('author', 'text')

#     # def post_str(self, obj: Comment) -> str:
#     #     link = reverse("admin:django_posts_and_comments_post_change",
#     #                    args=[obj.post.id])
#     #     return mark_safe(
#     #         f'<a href="{link}">{escape(obj.forum_post.__str__())}</a>')

#     #post_str.short_description = 'Post' # type: ignore
#     # make row sortable
#     #post_str.admin_order_field = 'post'  # type: ignore