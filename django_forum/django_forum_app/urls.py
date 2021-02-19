from django.urls import path, include
from .profile_views import ForumProfileUpdateView, \
                           ForumProfileImageDeleteView, \
                           ForumProfileUploadView
from .views import LandingPageView, \
                   ForumPostListView, \
                   ForumPostView, \
                   ForumPostCreateView \
                   #posts_search, autocomplete
from .forms import ForumPostCreateForm
from .models import ForumPost

app_name="django_forum_app"
urlpatterns = [
    path('users/accounts/profile/', ForumProfileUpdateView.as_view(), 
                                name='profile_update_view'),
    path('users/accounts/profile/images/update/', ForumProfileUploadView.as_view(), name='image_update'),
    path('user/accounts/profile/images/update/<slug:unique_id>/', ForumProfileImageDeleteView.as_view(), name='remove_images'),
    path('forum/create_post/', ForumPostCreateView.as_view(), name='post_create_view'),
    path('forum/posts/<slug:search_slug>', ForumPostListView.as_view(), name='post_list_view'),
    path('forum/posts/', ForumPostListView.as_view(), name='post_list_view'),
    path('forum/<int:pk>/<slug:post_slug>/', ForumPostView.as_view(), name='post_view'),
    path('', LandingPageView.as_view(), name='landing_page'),
    # path('posts_search/', posts_search, name='custom-search'),
    # path('autocomplete/', autocomplete, name='autocomplete')
]