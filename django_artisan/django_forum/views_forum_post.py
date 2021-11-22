from django import http, shortcuts, urls, views
from django.contrib.auth import mixins

from . import models as forum_models


class DeletePost(mixins.LoginRequiredMixin, views.View):
	http_method_names = [ 'post' ]
	model = forum_models.ForumPost

	def post(self, *args, **kwargs):
		try:
			self.model.objects.get(id=kwargs['pk']).delete()
		except ObjectDoesNotExist:
			logger.warn('the model you tried to delete does not exist')

		return shortcuts.redirect(urls.reverse_lazy('django_forum:post_list_view'))