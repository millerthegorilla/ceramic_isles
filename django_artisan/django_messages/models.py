from django import conf
from django.db import models, DEFAULT_DB_ALIAS
from django.contrib import auth

from . import soft_deletion
# Create your models here.


class Message(soft_deletion.Model):
    author: models.ForeignKey = models.ForeignKey(
        auth.get_user_model(), on_delete=models.SET_NULL, null=True, related_name="%(app_label)s_%(class)s_related")
    text: models.TextField = models.TextField(max_length=500)
    moderation_date: models.DateField = models.DateField(null=True, default=None, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    slug: models.SlugField = models.SlugField(unique=True, db_index=True, max_length=80)

    def get_author_name(self) -> str:
        return self.author.username

    def __str__(self) -> str:
        return f"{self.author.username}"

    class Meta:
        try:
            abstract = conf.settings.ABSTRACTMESSAGE
        except AttributeError:
            abstract = False


# class Moderation(models.Model):
#     author: models.ForeignKey = models.ForeignKey(
#         auth.get_user_model(), on_delete=models.SET_NULL, null=True, related_name="moderations")
#     moderation_date: models.DateField = models.DateField(null=True, default=None, blank=True)

#     class Meta:
#         abstract = True
    
