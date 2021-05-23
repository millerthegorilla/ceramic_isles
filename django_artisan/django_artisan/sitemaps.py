from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django_artisan.models import ArtisanForumProfile

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['about_view', 'register', 'landing_page', 'login', 'rules_view']

    def location(self, item):
        return reverse(item)

class PersonalPageSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ArtisanForumProfile.objects.all().filter(display_personal_page=True).values('display_name')

    def location(self, item):
        return  '/people/' + str(item)
