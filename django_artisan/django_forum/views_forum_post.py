import bleach, html, logging, uuid

from django_q import tasks

from django import http, shortcuts, urls, views, utils, conf
from django.core import mail
from django.contrib import auth
from django.template import defaultfilters
from django.db.models import F
from django.views.decorators import cache
from django.utils import timezone, decorators
from django.contrib.sites import models as site_models


from django_messages import views as messages_views

from . import models as forum_models
from . import forms as forum_forms

logger = logging.getLogger('django_artisan')


def send_mod_mail(type: str) -> None:
    mail.send_mail(
        'Moderation for {0}'.format(type),
        'A {0} has been created and requires moderation.  Please visit the {1} AdminPanel, and inspect the {0}'.format(
            type,
            conf.settings.SITE_NAME),
        conf.settings.EMAIL_HOST_USER,
        list(
            auth.get_user_model().objects.filter(
                is_staff=True).values_list(
                'email',
                flat=True)),
        fail_silently=False,
    )


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
@utils.decorators.method_decorator(cache.never_cache, name='get')
class PostView(messages_views.MessageView):
    """
        TODO: Replace superclass form processing if conditions with separate urls/views
              and overload them individually here, where necessary, instead of redefining
              the whole if clause.
    """
    # model: forum_models.Post = forum_models.Post
    # slug_url_kwarg: str = 'slug'
    # slug_field: str = 'slug'
    template_name: str = 'django_forum/posts_and_comments/forum_post_detail.html'
    # form_class: forum_forms.Post = forum_forms.Post
    comment_form_class: forum_forms.Comment = forum_forms.Comment

    def get(self, request: http.HttpRequest, pk:int, slug:str) -> http.HttpResponse:
        self.object = self.get_object()
        context = self.get_context_data()
        return shortcuts.render(self.request,
                      self.template_name,
                      context)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        site = site_models.Site.objects.get_current()
        context_data['site_url'] = (self.request.scheme or 'https') + '://' + site.domain
        context_data['comment_form'] = self.comment_form_class() # type: ignore
        context_data['subscribed'] = self.object.subscribed_users.filter(username=self.request.user.username).count()
        context_data['comments'] = self.object.comments.all()
        return context_data


#ajax function for subscribe checkbox
def subscribe(request) -> http.JsonResponse:
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        try:
            fp = forum_models.Post.objects.get(slug=request.POST['slug'])
            if request.POST['data'] == 'true':
                fp.subscribed_users.add(request.user)
            else:
                fp.subscribed_users.remove(request.user)
            return http.JsonResponse({}, status=200)
        except forum_models.Post.DoesNotExist as e:
            logger.error('There is no post with that slug : {0}'.format(e))
            return http.JsonResponse(
                {"error": "no post with that slug"}, 
                status=500)
    else:
        return http.JsonResponse(
            {"error": ""}, 
            status=500)

class PostUpdate(auth.mixins.LoginRequiredMixin, messages_views.MessageUpdate):
    model = forum_models.Post
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest, 
                   pk: int, slug:str, post:forum_models.Post = None,
                   updatefields:list = []) -> http.HttpResponseRedirect:
        try:
            if post is None:
                post = self.model.objects.get(id=pk)
            post.text = messages_views.sanitize_post_text(self.request.POST['update-post'])
            post.save(update_fields=['text'] + updatefields)
            return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view', args=[pk, slug]))
        except self.model.DoesNotExist:
            logger.error('post does not exist when updating post.')
  

class DeletePost(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    model = forum_models.Post
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest, pk: int, slug:str) -> http.HttpResponseRedirect:
        post = self.model.objects.get(id=pk, slug=slug)
        if post.author == request.user:
            try:
                post.delete()
            except self.model.DoesNotExist:
                logger.warn('the model you tried to delete does not exist')

        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_list_view'))


class CreateComment(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names: list = ['post']
    post_model: forum_models.Post = forum_models.Post
    comment_model: forum_models.Comment = forum_models.Comment
    form_class: forum_forms.Comment = forum_forms.Comment
    template_name: str = 'django_forum/posts_and_comments/forum_post_detail.html'
    a_name: str = 'django_forum'

    def post(self, request: http.HttpRequest, pk:int, slug:str):
        post = self.post_model.objects.get(pk=pk)
        if not post.moderation_date:
            comment_form = self.form_class(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user
                new_comment.text = bleach.clean(
                    html.unescape(new_comment.text), strip=True)
                new_comment.slug = defaultfilters.slugify(new_comment.text[:4] + '_comment_' 
                                   + str(new_comment.created_at or utils.timezone.now()))
                new_comment.forum_post = post
                new_comment.save()
                sname: str = "subscribe_timeout" + str(uuid.uuid4())
                tasks.schedule('django_forum.tasks.send_susbcribed_email',
                             name=sname,
                             schedule_type="O",
                             repeats=-1,
                             next_run=utils.timezone.now() + conf.settings.COMMENT_WAIT,
                             post_id=post.id,
                             comment_id=new_comment.id,
                             s_name=sname,
                             path_info=self.request.path_info)
                return shortcuts.redirect(new_comment)
            else:
                site = site_models.Site.objects.get_current()
                comments = self.model.objects.filter(post_fk=post).all()
                return shortcuts.render(self.request,
                             self.template_name,
                             {'comment_edit': True,
                              'post': post,
                              'comments': comments,
                              'comment_form': comment_form,
                              'site_url': (self.request.scheme or 'https') + '://' + site.domain})
        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view', 
                                                    args=[post.id, post.slug]))


class DeleteComment(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    post_model = forum_models.Post
    comment_model = forum_models.Comment
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        comment = self.comment_model.objects.get(id=request.POST['comment-id'],
                                                 slug=request.POST['comment-slug'])
        post = self.post_model.objects.get(id=request.POST['post-id'], 
                                           slug=request.POST['post-slug'])
        if comment.author == request.user:
            try:
                comment.delete()
            except self.model.DoesNotExist:
                logger.warn('the model you tried to delete does not exist')

        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view',
                                                    args=[post.id, post.slug]))


class UpdateComment(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    comment_model = forum_models.Comment
    post_model = forum_models.Post
    a_name = 'django_forum'
    
    def post(self, request:http.HttpRequest) -> http.HttpResponseRedirect:
        comment = self.comment_model.objects.get(id=request.POST['comment-id'],
                                                 slug=request.POST['comment-slug'])
        post = self.post_model.objects.get(id=request.POST['post-id'], 
                                           slug=request.POST['post-slug'])
        if comment.author == request.user:
            comment.text = request.POST['comment-text']
            comment.save(update_fields=['text'])
        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view',
                                                    args=[post.id, post.slug])
                                                    + '#' + comment.slug)


class ReportComment(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    comment_model = forum_models.Comment
    post_model = forum_models.Post
    a_name = 'django_forum'
    
    def post(self, request:http.HttpRequest) -> http.HttpResponseRedirect:
        comment = self.comment_model.objects.get(id=request.POST['comment-id'],
                                                 slug=request.POST['comment-slug'])
        post = self.post_model.objects.get(id=request.POST['post-id'], 
                                           slug=request.POST['post-slug'])
        if comment.author != request.user:
            comment.moderation_date = utils.timezone.now()
            comment.save(update_fields=['moderation_date'])
            send_mod_mail('Comment')
        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view',
                                                    args=[post.id, post.slug])
                                                    + '#' + comment.slug)


class ReportPost(auth.mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    post_model = forum_models.Post
    a_name = 'django_forum'
    
    def post(self, request:http.HttpRequest) -> http.HttpResponseRedirect:
        post = self.post_model.objects.get(id=request.POST['post-id'], 
                                           slug=request.POST['post-slug'])
        if post.author != request.user:
            post.moderation_date = utils.timezone.now()
            post.save(update_fields=['moderation_date'])
            send_mod_mail('Post')
        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view',
                                                    args=[post.id, post.slug]))
