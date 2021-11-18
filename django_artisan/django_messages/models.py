from django.db import models
from django.contrib import auth

from . import soft_deletion
# Create your models here.


class Message(soft_deletion.Model):
	author: models.ForeignKey = models.ForeignKey(
	    auth.get_user_model(), on_delete=models.SET_NULL, null=True, related_name="messages")
	text: models.TextField = models.TextField(max_length=500)
	created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	slug: models.SlugField = models.SlugField(unique=True, db_index=True, max_length=80)
