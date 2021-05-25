"""django_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django_email_verification import urls as mail_urls
from django_users_app import urls as users_app_urls
from django_forum_app import urls as forum_app_urls
from django_artisan import urls as artisan_app_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib.staticfiles import views
from django.contrib.sitemaps.views import sitemap
from django_artisan.sitemaps import StaticViewSitemap, PersonalPageSiteMap
from django_forum_app.views import CustomRegisterView
# from django.contrib.sites.models import Site

# current_site = Site.objects.all().first()
# current_site.domain_name = "127.0.0.1:8000"
# current_site.name = "127.0.0.1:8000"
# current_site.save()

sitemaps = { 'main': StaticViewSitemap,
             'personalpage': PersonalPageSiteMap }

urlpatterns = [
    path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),
    path('', include(artisan_app_urls)),
    path('forum/', include(forum_app_urls)),
    path('users/', include(users_app_urls)),
    path('email/', include(mail_urls)),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

try:
    settings.DEBUG
except NameError:
    pass # log that we are not debug
else:
    if settings.DEBUG == True:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns