from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django_artisan.models import ArtisanForumProfile
from typing import Any, List


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self) -> List[str]:
        return [
            'about_view',
            'register',
            'landing_page',
            'login',
            'rules_view']

    def location(self, item) -> Any:
        return reverse(item)


class PersonalPageSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self) -> Any:
        return ArtisanForumProfile.objects.all().filter(
            display_personal_page=True).values('display_name')

    def location(self, item) -> str:
        return '/people/' + str(item)
