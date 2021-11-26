import bleach, logging

from django import http, shortcuts, urls, views
from django.contrib.auth import mixins

from django_forum import views_forum_post as forum_post_views

from . import models as artisan_models

logger = logging.getLogger('django_artisan')


class ArtisanForumPostUpdate(forum_post_views.ForumPostUpdate):
    model = artisan_models.ArtisanForumPost
    a_name = 'django_artisan'

    def post(self, request: http.HttpRequest, pk: int, slug:str) -> http.HttpResponseRedirect:
        try:
            post = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            logger.error('post does not exist when updating post.')
        post.category = self.request.POST['category']
        post.location = self.request.POST['location']
        post.save(update_fields=['category', 'location'])
        return super().post(request, pk, slug, post, updatefields=['category', 'location'])