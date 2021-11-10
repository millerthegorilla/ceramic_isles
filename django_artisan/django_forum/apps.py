from django.apps import AppConfig
from django.db.models.signals import pre_init, post_save, pre_save, post_delete, pre_delete


class DjangoForumAppConfig(AppConfig):
    name = 'django_forum'

    # def ready(self):
    # 	post_save.connect(my_handler, ParentClass)
    # 	# connect all subclasses of base content item too
    # 	for subclass in ParentClass.__subclasses__():
    # 	    post_save.connect(my_handler, subclass)
