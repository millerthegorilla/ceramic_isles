import bleach, logging

from django import http, shortcuts, urls, views, conf
from django.contrib.auth import mixins
from django.utils import decorators
from django.views.decorators import cache

from django_forum import views_forum_post as forum_post_views

from . import models as artisan_models
from . import forms as artisan_forms

logger = logging.getLogger('django_artisan')


@decorators.method_decorator(cache.never_cache, name='dispatch')
@decorators.method_decorator(cache.never_cache, name='get')
class PostView(forum_post_views.PostView):
    model: artisan_models.Post = artisan_models.Post
    slug_url_kwarg: str = 'slug'
    slug_field: str = 'slug'
    template_name: str = 'django_artisan/posts_and_comments/forum_post_detail.html'
    form_class: artisan_forms.Post = artisan_forms.Post

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category = self.object.get_category_display()
        cat_text = ''
        for i in [(cat.value, cat.label) for cat in conf.settings.CATEGORY]:
            if i[1] == category:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'
        location = self.object.get_location_display()
        loc_text = ''
        for i in [(loc.value, loc.label) for loc in conf.settings.LOCATION]:
            if i[1] == location:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'
        context_data['category_opts'] = cat_text
        context_data['location_opts'] = loc_text
        return context_data


class PostUpdate(forum_post_views.PostUpdate):
    model = artisan_models.Post
    a_name = 'django_artisan'

    def post(self, request: http.HttpRequest, pk: int, slug:str) -> http.HttpResponseRedirect:
        try:
            post = self.model.objects.get(id=pk)
        except self.model.DoesNotExist:
            logger.error('post does not exist when updating post.')
        bob = []
        if conf.settings.SHOW_CATEGORY:
            post.category = self.request.POST['category']
            bob.append('category')
        if conf.settings.SHOW_LOCATION:
            post.location = self.request.POST['location']
            bob.append('location')
        if len(bob):
            post.save(update_fields=bob)
        return super().post(request, pk, slug, post, updatefields=['category', 'location'])