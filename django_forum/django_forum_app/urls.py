from django.urls import path
from .profile_views import ForumProfileUpdateView, \
                           ForumProfileImageDeleteView, \
                           ForumProfileUploadView
from .views import LandingPageView, \
                   ForumPostCreateView, \
                   ForumPostListView, \
                   ForumPostView

urlpatterns = [
    path('users/accounts/profile/', ForumProfileUpdateView.as_view(), 
                                name='forum_profile_update_view'),
    path('users/accounts/profile/images/update/', ForumProfileUploadView.as_view(), name='forum_image_update'),
    path('user/accounts/profile/images/update/<slug:unique_id>/', ForumProfileImageDeleteView.as_view(), name='forum_remove_images'),
    path('forum/create_post/', ForumPostCreateView.as_view(), name='forum_post_create_view'),
    path('forum/posts/', ForumPostListView.as_view(), name='forum_post_list_view'),
    path('forum/<int:pk>/<slug:post_slug>/', ForumPostView.as_view(), name='post_view'),
    path('', LandingPageView.as_view(), name='landing_page')
]