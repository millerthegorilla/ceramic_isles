from django import dispatch
from django.db.models import signals
from django.contrib.auth import models as auth_models


@dispatch.receiver(signals.pre_save, sender=auth_models.User)
def set_is_active_to_false(sender: auth_models.User, instance: auth_models.User, created: bool = False, **kwargs) -> None:
    if created and instance.is_superuser is not True:
        instance.is_active = False
        instance.save()
