from django import apps


class DjangoUsers(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_users'
