from django import apps


class DjangoProfileConfig(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_profile'
