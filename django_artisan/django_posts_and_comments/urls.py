from django import urls
from . import views as posts_and_comments_views

app_name = 'django_posts_and_comments'

urlpatterns = [
    urls.path('posts/', posts_and_comments_views.PostList.as_view(), name='post_list_view'),
    urls.path('create_post/', posts_and_comments_views.PostCreate.as_view(), name='post_create_view'),
    urls.path('<int:pk>/<slug:slug>/', posts_and_comments_views.Post.as_view(), name='post_view'),
]
