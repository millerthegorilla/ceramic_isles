import dropbox
import logging

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.utils import log
from django.core import management
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.db.models import QuerySet

from django_password_validators.password_history.models import PasswordHistory

from django_forum.models import ForumProfile
from .models import UserProductImage, Event, ArtisanForumProfile


logger = logging.getLogger('django_artisan')


class DjangoArtisanConfig(AppConfig):
    name = 'django_artisan'

    def ready(self) -> None:
        post_migrate.connect(callback, sender=self)

def callback(sender: DjangoArtisanConfig, **kwargs) -> None:
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=settings.SITE_ID)
        if current_site.domain != settings.SITE_DOMAIN:
            raise ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN")
    except Site.DoesNotExist:
        logger.info("Creating Site Model with domain={0}, name={1}, id={2}".format(
            settings.SITE_DOMAIN, settings.SITE_NAME, settings.SITE_ID))
        Site.objects.create(domain=settings.SITE_DOMAIN,
                            name=settings.SITE_NAME, id=settings.SITE_ID)


@admin.register(UserProductImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'active', 'image_file',
        'image_shop_link',
        'image_title', 'image_text',
        'image_shop_link_title'
    )
    list_filter = (
        'active', 'image_file',
        'image_title'
    )
    search_fields = (
        'image_text', 'image_title',
        'image_shop_link'
    )
    actions = ['approve_image']

    def approve_image(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                '%d image was approved.',
                '%d images were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'active', 'title',
        'text', 'date',
        'repeating'
    )
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            ngettext(
                '%d event was approved.',
                '%d events were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )

    def disapprove_event(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(active=False)
        self.message_user(
            request,
            ngettext(
                '%d event was disapproved.',
                '%d events were disapproved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


# #admin.site.unregister(UserPasswordHistoryConfig)
admin.site.unregister(PasswordHistory)

admin.site.unregister(ForumProfile)

# Register your models here.


@admin.register(ArtisanForumProfile)
class ArtisanForumProfileAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 'bio',
        'image_file', 'shop_web_address',
        'outlets', 'listed_member',
        'display_personal_page', 'address_line_1',
        'address_line_2', 'parish',
        'postcode', 'avatar',
        'rules_agreed'
    ]
    list_filter = [
        'display_name', 'parish',
        'rules_agreed', 'shop_web_address',
        'listed_member', 'display_personal_page'
    ]
    search_fields = [
        'display_name', 'address_line_1',
        'parish', 'bio'
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)


# TODO switch from dbbackup to runrestic to use restic - https://restic.net/
class tasks:
    def db_backup(self) -> None:
        # clear existing backups first - dbbackup --clean doesn't work with
        # dropbox.
        try:
            dbx = dropbox.Dropbox(
                settings.DBBACKUP_STORAGE_OPTIONS['oauth2_access_token'])
        except dropbox.exceptions.AuthError as e:
            logger.error("Dropbox Auth Issue : {0}".format(e))
        except dropbox.exceptions.HttpError as e:
            logger.error("Dropbox HttpError : {0}".format(e))
        for entry in dbx.files_list_folder('', recursive=True).entries:
            dbx.files_delete(entry.path_display)
        management.call_command("dbbackup --traceback")
        management.call_command("mediabackup")
        logger.info("succesfully backed up database and media files")

    # def ping_google():
    #     """
    #         You must be registered with google search console for this to work
    #         ... https://search.google.com/search-console/welcome
    #     """
    #     management.call_command("ping_google")
