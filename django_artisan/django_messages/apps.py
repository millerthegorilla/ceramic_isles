from django import apps


"""
    This app is purely an abstraction at the moment, of the commonalities
    between posts and comments.  It seems like a good idea, in the sense that
    I can in the future, flesh out the messages app for use as messages in a
    messaging system of some kind.  Which is why I am not making it an ABC, and 
    giving it its own app.
"""


class DjangoMessagesConfig(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_messages'
