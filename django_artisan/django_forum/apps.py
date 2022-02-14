from django import apps
from django.conf import settings
from django.core import exceptions
from django.db import models

class DjangoForum(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_forum'

    def ready(self) -> None:
        models.signals.post_migrate.connect(callback, sender=self)

## the below is for sites framework but getting the current site is a hideously long query
## so better to replace need with conf.settings.SITE_DOMAIN etc...
def callback(sender: DjangoForum, **kwargs) -> None:
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=settings.SITE_ID)
        if current_site.domain == "example.com":
            current_site.domain = settings.SITE_DOMAIN
            current_site.name = settings.SITE_NAME
            #current_site.id = settings.SITE_ID
            current_site.save()
        elif current_site.domain != settings.SITE_DOMAIN:
            raise exceptions.ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN")
    except Site.DoesNotExist:
        Site.objects.create(domain=settings.SITE_DOMAIN,
                            name=settings.SITE_NAME, id=settings.SITE_ID)
