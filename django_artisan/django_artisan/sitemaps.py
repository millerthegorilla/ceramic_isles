import typing

from django import urls
from django.contrib import sitemaps
from django.db import models as db_models

from django_artisan import models as artisan_models


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self) -> typing.List[str]:
        return [
            'about_view',
            'register',
            'landing_page',
            'login',
            'rules_view']

    def location(self, item) -> str:
        return urls.reverse(item)


class PersonalPageSiteMap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self) -> db_models.QuerySet:
        return artisan_models.ArtisanForumProfile.objects.all().filter(
            display_personal_page=True).values('display_name')

    def location(self, item) -> str:
        return '/people/' + str(item)
