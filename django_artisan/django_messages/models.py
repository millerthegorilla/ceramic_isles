from django.db import models

from . import soft_deletion
# Create your models here.


class Message(soft_deletion.Model):
	author: models.CharField = models.CharField(default='', max_length=40)
	text: models.TextField = models.TextField(max_length=500)
	date_created: models.DateTimeField = models.DateTimeField(auto_now_add=True)