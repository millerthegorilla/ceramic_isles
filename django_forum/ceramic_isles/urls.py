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
import debug_toolbar
from django_email_verification import urls as mail_urls
from django_users_app import urls as users_app_urls
#from django_profile import urls as profile_urls
from django_forum_app import urls as forum_app_urls
from django_artisan import urls as artisan_app_urls
#from django_posts_and_comments import urls as p_c_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib.staticfiles import views
from django_forum_app.views import CustomRegisterView

urlpatterns = [
    path('', include(artisan_app_urls)),
    path('forum/', include(forum_app_urls)),
   # path('forum/', include(p_c_urls)),
   # path('profile/', include(profile_urls)),
    path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),
    path('users/', include(users_app_urls)),
    path('email/', include(mail_urls)),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(urlpatterns)
# if settings.DEBUG:
#     urlpatterns += [
#             re_path(r'^static/(?P<path>.*)$', views.serve),
#         ]
