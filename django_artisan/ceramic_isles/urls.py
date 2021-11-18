import logging

from django.contrib import admin
from django.urls import include, path
from django_email_verification import urls as mail_urls
from django_users import urls as users_app_urls
from django_forum import urls as forum_urls
from django_artisan import urls as artisan_urls
from django_messages import urls as messages_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, URLResolver
from django.contrib.staticfiles import views
from django.contrib.sitemaps.views import sitemap
from django_artisan.sitemaps import StaticView, PersonalPage
from django_artisan import views as artisan_views
from django_forum.views import CustomRegister

logger = logging.getLogger('django_artisan')

sitemaps = {'main': StaticView,
            'personalpage': PersonalPage}

urlpatterns = [
    path('users/accounts/register/', CustomRegister.as_view(), name='register'),
    path('', include(artisan_urls)),
    path('forum/', include(forum_urls)),
    # path('forum/create_post/', artisan_views.ArtisanForumPostCreate.as_view(), name='post_create_view'),
    path('messages/', include(messages_urls)),
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
    if settings.DEBUG:
        logger.info("Django is in debug mode")
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    else:
        logger.info("Django is in production mode")
