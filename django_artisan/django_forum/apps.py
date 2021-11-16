from django import apps


class DjangoForumAppConfig(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_forum'
