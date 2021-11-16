from django import apps


class DjangoPostsAndComments(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_posts_and_comments'
