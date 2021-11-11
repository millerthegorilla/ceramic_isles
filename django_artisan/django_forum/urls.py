from django import urls

from . import views as forum_views 

app_name = "django_forum"
urlpatterns = [
    urls.path('profile/', forum_views.ForumProfile.as_view(),
         name='profile_update_view'),
    urls.path(
        'create_post/',
        forum_views.ForumPost.as_view(),
        name='post_create_view'),
    urls.path('posts/<slug:search_slug>',
         forum_views.ForumPostList.as_view(), name='post_list_view'),
    urls.path('posts/', forum_views.ForumPostList.as_view(), name='post_list_view'),
    urls.path(
        '<int:pk>/<slug:post_slug>/',
        forum_views.ForumPostView.as_view(),
        name='post_view'),
    urls.path('rules/', forum_views.RulesPageView.as_view(), name='rules_view'),
    urls.path('register/', forum_views.CustomRegister.as_view(), name='register'),
    urls.path('subscribe/', forum_views.subscribe, name='subscribe')
    # path('autocomplete/', autocomplete, name='autocomplete')  # experimental
    # autocomplete
]

# NEEDED FOR ADDITION OF DISPLAY_NAME AND RULES
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),
