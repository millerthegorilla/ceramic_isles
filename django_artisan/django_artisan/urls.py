from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django_forum_app.views import ForumPostView, ForumPostListView

from .views import AboutPageView, LandingPageView, PersonalPageView, \
    UserProductImageUploadView, UserProductImageDeleteView, \
    ArtisanForumProfileUpdateView

admin.site.site_header = settings.SITE_NAME + ' admin'
admin.site.site_title = settings.SITE_NAME + ' admin'
admin.site.site_url = 'https://' + settings.SITE_DOMAIN
admin.site.index_title = settings.SITE_NAME + ' administration'
admin.empty_value_display = '**Empty**'

app_name = "django_artisan"
urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('about/', AboutPageView.as_view(), name='about_view'),
    path('people/<slug:name_slug>/',
         PersonalPageView.as_view(), name='personal_page_view'),
    path('users/accounts/profile/',
         ArtisanForumProfileUpdateView.as_view(), name='profile_update_view'),
    path('users/accounts/profile/images/update/',
         UserProductImageUploadView.as_view(), name='image_update'),
    path('users/accounts/profile/images/update/<slug:unique_id>/',
         UserProductImageDeleteView.as_view(), name='remove_images'),
    path('forum/posts/<slug:search_slug>', ForumPostListView.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_list.html'), name='post_list_view'),
    path('forum/posts/', ForumPostListView.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_list.html'), name='post_list_view'),
    path('forum/<int:pk>/<slug:post_slug>/', ForumPostView.as_view(
        template_name='django_artisan/posts_and_comments/forum_post_detail.html'), name='post_view'),
]
