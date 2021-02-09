from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_init, post_save
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def set_is_active_to_false(sender, instance, created, **kwargs):
	if created and instance.is_superuser is not True:
		instance.is_active = False
		instance.save()