import bleach, html, logging, typing

from django import conf, urls, utils, db, shortcuts, http
from django.core import exceptions, paginator
from django.views import generic
from django.template import defaultfilters

from django import db
from django.views.decorators import cache
from django.contrib.auth import mixins

from . import models as messages_models
from . import forms as messages_forms

logger = logging.getLogger('django_artisan')

def sanitize_post_text(text: str) -> utils.safestring.SafeString:
    return utils.safestring.mark_safe(bleach.clean(html.unescape(text),
                                  tags=conf.settings.ALLOWED_TAGS,
                                  attributes=conf.settings.ATTRIBUTES,
                                  styles=conf.settings.STYLES,
                                  strip=True, strip_comments=True))


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
class MessageList(generic.list.ListView):
    model = messages_models.Message
    template_name = 'django_messages/message_list.html'
    paginate_by = 6

    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        queryset = message_models.Message.objects.all()
        paginator = paginator.Paginator(queryset, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return shortcuts.render(request, self.template_name, context)


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
@utils.decorators.method_decorator(cache.never_cache, name='get')
class MessageView(generic.DetailView):
    """
        TODO: replace the single view/many form processing with separate urls for
              each form action, pointing to individual views, each with its own form class,
              each redirecting to this url/view with its get_context_data, for all forms.
    """
    model = messages_models.Message
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    template_name = 'django_messages/message.html'
    form_class = messages_forms.Message

    def get(self, *args, **kwargs) -> http.HttpResponse:
        message = messages_models.Message.objects.get(pk=kwargs['pk'])
        return shortcuts.render(self.request,
                      self.template_name,
                      { 'message': message })


class MessageUpdate(generic.detail.DetailView):
    model = messages_models.Message
    template_name = 'django_messages/message_detail.html'


class MessageDelete(generic.edit.DeleteView):
    model = messages_models.Message
    template_name = 'django_messages/message_detail.html'


class MessageCreate(generic.edit.CreateView):
    model = messages_models.Message
    template_name_suffix = '_create_form'
    #template_name = 'django_messages/message_create_form.html'
    form_class = messages_forms.Message

    def form_valid(self, form, message: messages_models.Message = None, **kwargs) -> http.HttpResponseRedirect:
        if message is None:
            message = form.save(commit=False)
        else:
            passed_message=True
        message.text = sanitize_post_text(message.text)       
        message.author = self.request.user
        message.slug = defaultfilters.slugify(
            message.text[:10] + '-' + str(utils.dateformat.format(utils.timezone.now(), 'Y-m-d H:i:s')))
        #super().form_valid(form)
        try:
            message.save()
        except db.IntegrityError as e:
            logger.error("Unable to create message : " + str(e))
        if passed_message:
            return message
        else:
            return shortcuts.redirect(self.get_success_url(message))

    def get_success_url(self, message, *args, **kwargs) -> str:
        return urls.reverse_lazy(
            'django_messages:message_view', args=(
                message.id, message.slug,))