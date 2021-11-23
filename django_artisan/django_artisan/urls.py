from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django_forum import views as forum_views
from django_forum import views_forum_post as forum_post_views

from . import views as artisan_views
from . import models as artisan_models

admin.site.site_header = settings.SITE_NAME + ' admin'
admin.site.site_title = settings.SITE_NAME + ' admin'
admin.site.site_url = 'https://' + settings.SITE_DOMAIN
admin.site.index_title = settings.SITE_NAME + ' administration'
#admin.empty_value_display = '**Empty**'

app_name = "django_artisan"

post_patterns = [
    path('update_post/', forum_views.ForumPostUpdate.as_view(),
               name='post_update'),
    path('delete_post/<int:pk>/<slug:slug>/', forum_post_views.DeletePost.as_view(
                                      model=artisan_models.ArtisanForumPost,
                                      a_name='django_artisan'
                                  ), name="post_delete"),
    path('save_comment/<int:pk>/<slug:slug>/', forum_post_views.SaveComment.as_view(
                              post_model=artisan_models.ArtisanForumPost,
                              template_name='django_artisan/posts_and_comments/forum_post_detail.html',
                              a_name=app_name), name="comment_save"),

]

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
    path('forum/create_post/', artisan_views.ArtisanForumPostCreate.as_view(), name='post_create_view'),
    path('forum/posts/', artisan_views.ArtisanForumPostList.as_view(model=artisan_models.ArtisanForumPost,
        template_name='django_artisan/posts_and_comments/forum_post_list.html'), name='post_list_view'),
    path('forum/<int:pk>/<slug:slug>', artisan_views.ArtisanForumPostView.as_view(), name='post_view'),
] + post_patterns
