from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django_forum import views as forum_views

from . import views as artisan_views

admin.site.site_header = settings.SITE_NAME + ' admin'
admin.site.site_title = settings.SITE_NAME + ' admin'
admin.site.site_url = 'https://' + settings.SITE_DOMAIN
admin.site.index_title = settings.SITE_NAME + ' administration'
#admin.empty_value_display = '**Empty**'

app_name = "django_artisan"
urlpatterns = [
    path('', artisan_views.LandingPage.as_view(), name='landing_page'),
    path('about/', artisan_views.AboutPage.as_view(), name='about_view'),
    path('people/<slug:name_slug>/',
         artisan_views.PersonalPage.as_view(), name='personal_page_view'),
    path('users/accounts/profile/',
         artisan_views.ArtisanForumProfile.as_view(), name='profile_update_view'),
    path('users/accounts/profile/images/update/',
         artisan_views.UserProductImageUpload.as_view(), name='image_update'),
    path('users/accounts/profile/images/update/<slug:unique_id>/',
         artisan_views.UserProductImageDelete.as_view(), name='remove_images'),
    path('forum/posts/<slug:search_slug>', forum_views.ForumPostList.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_list.html'), name='post_list_view'),
    path('forum/posts/', forum_views.ForumPostList.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_list.html'), name='post_list_view'),
    path('forum/<int:pk>/<slug:slug>/', forum_views.ForumPostView.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_detail.html'), name='post_view'),
]
