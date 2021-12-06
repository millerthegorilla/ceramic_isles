from django import urls

from . import views as forum_views
from . import views_forum_post as forum_post_views 

app_name = "django_forum"

postview_patterns = [
    urls.path('<int:pk>/<slug:slug>/', forum_post_views.ForumPostView.as_view(),
                name='post_view'),
    urls.path('update_post/<int:pk>/<slug:slug>/', forum_post_views.ForumPostUpdate.as_view(),
                name='post_update'),
    urls.path('delete_post/<int:pk>/', forum_post_views.DeletePost.as_view(),
                name="post_delete"),
    urls.path('report_post/', forum_post_views.ReportPost.as_view(),
                name='post_report'),
    urls.path('create_comment/<int:pk>/<slug:slug>/', forum_post_views.CreateComment.as_view(), 
                name="comment_create"),
    urls.path('delete_comment/', forum_post_views.DeleteComment.as_view(),
                name='comment_delete'),
    urls.path('update_comment/', forum_post_views.UpdateComment.as_view(),
                name='comment_update'),
    urls.path('report_comment/', forum_post_views.ReportComment.as_view(),
                name='comment_report'),
    urls.path('subscribe/', forum_post_views.subscribe, name='subscribe')
]

urlpatterns = [
    urls.path('create_post/', forum_views.ForumPostCreate.as_view(),
                name='post_create_view'),
    urls.path('posts/', forum_views.ForumPostList.as_view(),
                name='post_list_view'),
    urls.path('profile/', forum_views.ForumProfile.as_view(),
         name='profile_update_view'),
    urls.path('rules/', forum_views.RulesPageView.as_view(), name='rules_view'),
    urls.path('register/', forum_views.CustomRegister.as_view(), name='register'),
    # path('autocomplete/', autocomplete, name='autocomplete')  # experimental
    # autocomplete
] + postview_patterns



# NEEDED FOR ADDITION OF DISPLAY_NAME AND RULES
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),
