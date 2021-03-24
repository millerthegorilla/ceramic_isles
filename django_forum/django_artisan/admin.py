from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from django_password_validators.password_history.models import PasswordHistory

from django_forum_app.models import ForumProfile
from .models import UserProductImage, Event, ArtisanForumProfile


@admin.register(UserProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('active', 'image_file', 'image_shop_link', 'image_title', 'image_text', 'image_shop_link_title')
    list_filter = ('active', 'image_file', 'image_title')
    search_fields = ('image_text', 'image_title', 'image_shop_link')
    actions = ['approve_image']

    def approve_image(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, ngettext(
                    '%d image was approved.',
                    '%d images were approved.',
                    updated,
                ) % updated, messages.SUCCESS)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('active', 'title', 'text', 'date', 'repeating')
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, ngettext(
                    '%d event was approved.',
                    '%d events were approved.',
                    updated,
                ) % updated, messages.SUCCESS)

    def disapprove_event(self, request, queryset):
        updated = queryset.update(active=False)       
        self.message_user(request, ngettext(
                    '%d event was disapproved.',
                    '%d events were disapproved.',
                    updated,
                ) % updated, messages.SUCCESS)

# #admin.site.unregister(UserPasswordHistoryConfig)
admin.site.unregister(PasswordHistory)

admin.site.unregister(ForumProfile)

# Register your models here.
@admin.register(ArtisanForumProfile)
class ArtisanForumProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'bio', 'image_file', 'shop_web_address', 
                    'outlets', 'listed_member', 'display_personal_page', 
                    'address_line_1','address_line_2','parish','postcode',
                    'avatar','rules_agreed']
    list_filter = ['display_name','parish','rules_agreed', 'shop_web_address',
                   'listed_member', 'display_personal_page']
    search_fields = ['display_name','address_line_1', 'parish', 'bio']

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)