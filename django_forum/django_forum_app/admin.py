from django.contrib import admin
from .models import ForumProfileImage

@admin.register(ForumProfileImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'image_text', 'image_title', 'image_shop_link', 'image_shop_link_title', 'active')
    list_filter = ('active', 'image_file')
    search_fields = ('image_text', 'image_title', 'image_shop_link')
    actions = ['approve_image']

    def approve_image(self, request, queryset):
        queryset.update(active=True)