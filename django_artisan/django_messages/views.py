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
class MessageList(mixins.LoginRequiredMixin, generic.list.ListView):
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
class MessageView(mixins.LoginRequiredMixin, generic.DetailView):
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

    # def post(self, *args, **kwargs) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]:
    #     post = posts_and_comments_models.Post.objects.get(pk=kwargs['pk'])
    #     if self.request.POST['type'] == 'post' and \
    #        self.request.user.profile.display_name == post.post_author():
    #         post.delete()
    #         return shortcuts.redirect(
    #             urls.reverse_lazy('django_posts_and_comments:post_list_view'))
    #     elif self.request.POST['type'] == 'comment':
    #         comment_form = self.form_class(data=self.request.POST)
    #         if comment_form.is_valid():
    #             new_comment = comment_form.save(commit=False)
    #             new_comment.text = bleach.clean(
    #                 html.unescape(new_comment.text), strip=True)
    #             new_comment.post = post
    #             new_comment.user_profile = self.request.user.profile
    #             new_comment.save()
    #             return shortcuts.redirect(post)
    #         else:
    #             comments = posts_and_comments_models.Comment.objects.filter(post=post).all()
    #             return shortcuts.render(
    #                 self.request, self.template_name, {
    #                     'post': post, 'comments': comments, 'comment_form': comment_form})
    #     elif self.request.POST['type'] == 'update':
    #         post.text = self.request.POST['update-post']
    #         post.save(update_fields=['text'])
    #         return shortcuts.redirect(post)
    #     elif self.request.POST['type'] == 'rem-comment':
    #         posts_and_comments_models.Comment.objects.get(pk=self.request.POST['comment']).delete()
    #         return shortcuts.redirect(post)
    #     elif self.request.POST['type'] == 'comment-update':
    #         try:
    #             comment = posts_and_comments_models.Comment.objects.get(id=self.request.POST['id'])
    #             comment.text = bleach.clean(html.unescape(
    #                 self.request.POST['comment-update']), strip=True)
    #             comment.save(update_fields=['text'])
    #             return shortcuts.redirect(post)
    #         except exceptions.ObjectDoesNotExist as e:
    #             logger.error("Error accessing comment : {0}".format(e))
    #             return shortcuts.redirect(post)
    #     else:
    #         logger.warn("request has no processable type")
    #         return shortcuts.redirect('django_posts_and_comments:post_list_view')

    def get(self, *args, **kwargs) -> http.HttpResponse:
        message = messages_models.Message.objects.get(pk=kwargs['pk'])
        return shortcuts.render(self.request,
                      self.template_name,
                      { 'message': message })


class MessageUpdate(mixins.LoginRequiredMixin, generic.detail.DetailView):
    model = messages_models.Message
    template_name = 'django_messages/message_detail.html'


class MessageDelete(mixins.LoginRequiredMixin, generic.edit.DeleteView):
    model = messages_models.Message
    template_name = 'django_messages/message_detail.html'


class MessageCreate(mixins.LoginRequiredMixin, generic.edit.CreateView):
    model = messages_models.Message
    template_name_suffix = '_create_form'
    #template_name = 'django_messages/message_create_form.html'
    form_class = messages_forms.Message

    def form_valid(self, form, post: messages_models.Message = None, **kwargs) -> http.HttpResponseRedirect:
        super().form_valid(form)
        message = form.save(commit=False)
        message.text = sanitize_post_text(message.text)
        message.author = self.request.user
        message.slug = defaultfilters.slugify(
            message.text[:10] + '-' + str(utils.dateformat.format(utils.timezone.now(), 'Y-m-d H:i:s')))
        try:
            message.save()
        except db.IntegrityError as e:
            logger.error("Unable to create message : " + str(e))
        return shortcuts.redirect(self.get_success_url(message))

    def get_success_url(self, post, *args, **kwargs) -> str:
        return urls.reverse_lazy(
            'django_messages:message_view', args=(
                message.id, message.slug,))