from django.contrib import admin

from .models import UserProductImage, Event
from django_password_validators.password_history.models import UserPasswordHistoryConfig, PasswordHistory


@admin.register(UserProductImage)
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


# #admin.site.unregister(UserPasswordHistoryConfig)
# admin.site.unregister(PasswordHistory)