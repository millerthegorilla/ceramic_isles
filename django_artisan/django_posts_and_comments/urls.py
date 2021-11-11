from django import urls import include, path
from . import views as posts_and_comments_views

app_name = 'django_posts_and_comments'

urlpatterns = [
    urls.path('posts/', posts_and_comments_views.PostListView.as_view(), name='post_list_view'),
    urls.path('create_post/', posts_and_comments_views.PostCreateView.as_view(), name='post_create_view'),
    urls.path('<int:pk>/<slug:post_slug>/', posts_and_comments_views.PostView.as_view(), name='post_view'),
]
