from django.urls import include, path
from .views import PostView, PostListView, PostCreateView

app_name = 'django_posts_and_comments'
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list_view'),
    path('create_post/', PostCreateView.as_view(), name='post_create_view'),
    path('<int:pk>/<slug:post_slug>/', PostView.as_view(), name='post_view'),
]
