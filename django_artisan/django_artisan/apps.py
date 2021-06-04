from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def callback(sender, **kwargs):
    from django.contrib.sites.models import Site
    try:
        current_site = Site.objects.get(id=settings.SITE_ID)
        if current_site.domain == "example.com":
            current_site.domain = settings.SITE_DOMAIN
            current_site.name = settings.SITE_NAME
            current_site.id = settings.SITE_ID
            current_site.save() 
        elif current_site.domain != settings.SITE_DOMAIN:
            raise ImproperlyConfigured("SITE_ID does not match SITE_DOMAIN") 
    except Site.DoesNotExist:
        Site.objects.create(domain=settings.SITE_DOMAIN, name=settings.SITE_NAME, id=settings.SITE_ID)
    

class DjangoArtisanConfig(AppConfig):
    name = 'django_artisan'

    def ready(self):
        post_migrate.connect(callback, sender=self)
        #thread1 = threading.Thread(target=self.init_thread, args=())
        #thread1.start()
    
    # def init_thread(self):
    #     flag = self.apps.ready_event.wait(100)
    #     if flag:
    #         if not self.site_made:
    #             from django.contrib.sites.models import Site
    #             current_site = Site.objects.all().first()
    #             current_site.domain = "127.0.0.1:8000"
    #             current_site.name = "127.0.0.1:8000"
    #             current_site.save()
    #             self.site_made = True
    #     else:
    #         print("django_artisan ready thread timedout!")
