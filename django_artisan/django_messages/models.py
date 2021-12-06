from django.db import models, DEFAULT_DB_ALIAS
from django.contrib import auth

from . import soft_deletion
# Create your models here.


class Message(soft_deletion.Model):
    author: models.ForeignKey = models.ForeignKey(
        auth.get_user_model(), on_delete=models.SET_NULL, null=True, related_name="messages")
    text: models.TextField = models.TextField(max_length=500)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    moderation_date: models.DateField = models.DateField(null=True, default=None, blank=True)
    slug: models.SlugField = models.SlugField(unique=True, db_index=True, max_length=80)

    def get_author_name(self) -> str:
        return self.author.username

    def __str__(self) -> str:
        return f"{self.author.username}"
