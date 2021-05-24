from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django_artisan.models import ArtisanForumProfile

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['django_artisan:about_view', 'register', 'django_artisan:landing_page', 'login', 'django_forum_app:rules_view']

    def location(self, item):
        return reverse(item)

class PersonalPageSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        '''
    	    the order_by removes garbage warning about pagination.
        '''
        return ArtisanForumProfile.objects.all().filter(display_personal_page=True).values('display_name').order_by('pk')

    def location(self, item):
        return  '/people/' + item['display_name']