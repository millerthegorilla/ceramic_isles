import dropbox
import logging

from django import apps, conf, http
from django.contrib import admin, messages
from django.core import exceptions, management
from django.utils import translation, log
from django.db import models

from django_password_validators.password_history.models import PasswordHistory

from django_forum.models import ForumProfile
from .models import UserProductImage, Event, ArtisanForumProfile


logger = logging.getLogger('django_artisan')


class DjangoArtisan(apps.AppConfig):
    name = 'django_artisan'

    def ready(self) -> None:
        models.signals.post_migrate.connect(callback, sender=self)

def callback(sender: DjangoArtisan, **kwargs) -> None:
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=conf.settings.SITE_ID)
        if current_site.domain != conf.settings.SITE_DOMAIN:
            raise exceptions.ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN")
    except Site.DoesNotExist:
        logger.info("Creating Site Model with domain={0}, name={1}, id={2}".format(
            conf.settings.SITE_DOMAIN, conf.settings.SITE_NAME, conf.settings.SITE_ID))
        Site.objects.create(domain=conf.settings.SITE_DOMAIN,
                            name=conf.settings.SITE_NAME, id=conf.settings.SITE_ID)


@admin.register(UserProductImage)
class Image(admin.ModelAdmin):
    list_display = (
        'active', 'file',
        'shop_link',
        'shop_link_title',
        'title', 'text',
    )
    list_filter = (
        'active', 'file',
        'title'
    )
    search_fields = (
        'text', 'title',
        'shop_link'
    )
    actions = ['approve_image']

    def approve_image(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            translation.ngettext(
                '%d image was approved.',
                '%d images were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = (
        'active', 'title',
        'text', 'date',
        'repeating'
    )
    actions = ['approve_event', 'disapprove_event']

    def approve_event(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=True)
        self.message_user(
            request,
            translation.ngettext(
                '%d event was approved.',
                '%d events were approved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )

    def disapprove_event(self, request: http.HttpRequest, queryset: models.QuerySet) -> None:
        updated = queryset.update(active=False)
        self.message_user(
            request,
            translation.ngettext(
                '%d event was disapproved.',
                '%d events were disapproved.',
                updated,
            ) % updated,
            messages.SUCCESS
        )


# #admin.site.unregister(UserPasswordHistoryConfig)
admin.site.unregister(PasswordHistory)

try:
    abs_forum_profile = conf.settings.ABSTRACTFORUMPROFILE
except AttributeError:
    abs_forum_profile = False
if not abs_forum_profile:
    admin.site.unregister(ForumProfile)

# Register your models here.


@admin.register(ArtisanForumProfile)
class ArtisanForumProfile(admin.ModelAdmin):
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

    def get_queryset(self, request: http.HttpRequest) -> models.QuerySet:
        return super().get_queryset(request).exclude(profile_user__is_superuser=True)


# TODO switch from dbbackup to runrestic to use restic - https://restic.net/
class tasks:
    def db_backup(self) -> None:
        # clear existing backups first - dbbackup --clean doesn't work with
        # dropbox.
        try:
            dbx = dropbox.Dropbox(
                confg.settings.DBBACKUP_STORAGE_OPTIONS['oauth2_access_token'])
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
