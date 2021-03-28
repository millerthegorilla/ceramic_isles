from django.urls import path, include

from .views import ForumPostListView, \
                   ForumPostView, \
                   ForumPostCreateView, \
                   CustomRegisterView, \
                   ForumProfileUpdateView, \
                   RulesPageView
                   #autocomplete
from .forms import ForumPostCreateForm
from .models import ForumPost

app_name="django_forum_app"
urlpatterns = [
    path('profile/', ForumProfileUpdateView.as_view(), 
                                name='profile_update_view'),
    path('create_post/', ForumPostCreateView.as_view(), name='post_create_view'),
    path('posts/<slug:search_slug>', ForumPostListView.as_view(), name='post_list_view'),
    path('posts/', ForumPostListView.as_view(), name='post_list_view'),
    path('<int:pk>/<slug:post_slug>/', ForumPostView.as_view(), name='post_view'),
    path('rules/', RulesPageView.as_view(), name='rules_view'),
    path('register/', CustomRegisterView.as_view(), name='register')
    # path('autocomplete/', autocomplete, name='autocomplete')  # experimental autocomplete
]

### NEEDED FOR ADDITION OF DISPLAY_NAME AND RULES
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegisterView
# path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),