import logging

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

logger = logging.getLogger('django')

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
         name='django.contrib.sitemaps.views.sitemap'),
]

try:
    settings.DEBUG
except NameError:
    logger.info("settings.DEBUG is not defined")
else:
    if settings.DEBUG == True:
        logger.info("Django is in debug mode")
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    else:
        logger.info("Django is in production mode")
