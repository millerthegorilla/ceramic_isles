import bleach, html, logging, uuid

from django_q import tasks

from django import http, shortcuts, urls, views, utils, conf
from django.contrib.auth import mixins
from django.template import defaultfilters
from django.db.models import F

from django_messages import views as messages_views

from . import models as forum_models
from . import forms as forum_forms

logger = logging.getLogger('django_artisan')


class ForumPostUpdate(mixins.LoginRequiredMixin, messages_views.MessageUpdate):
    model = forum_models.ForumPost
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest, 
                   pk: int, slug:str, post:forum_models.ForumPost = None,
                   updatefields:list = []) -> http.HttpResponseRedirect:
        try:
            if post is None:
                post = self.model.objects.get(id=pk)
            post.text = messages_views.sanitize_post_text(self.request.POST['update-post'])
            post.save(update_fields=['text'] + updatefields)
            return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view', args=[pk, slug]))
        except self.model.DoesNotExist:
            logger.error('post does not exist when updating post.')
        
class DeletePost(mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    model = forum_models.ForumPost
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest, pk: int, slug:str) -> http.HttpResponseRedirect:
        post = self.model.objects.get(id=pk, slug=slug)
        if post.author == request.user:
            try:
                post.delete()
            except self.model.DoesNotExist:
                logger.warn('the model you tried to delete does not exist')

        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_list_view'))


class CreateComment(mixins.LoginRequiredMixin, views.View):
    http_method_names: list = ['post']
    post_model: forum_models.ForumPost = forum_models.ForumPost
    comment_model: forum_models.ForumComment = forum_models.ForumComment
    form_class: forum_forms.ForumComment = forum_forms.ForumComment
    template_name: str = 'django_forum/posts_and_comments/forum_post_detail.html'
    a_name: str = 'django_forum'

    def post(self, request: http.HttpRequest, pk:int, slug:str):
        post = self.post_model.objects.get(pk=pk)
        comment_form = self.form_class(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = post.author
            new_comment.text = bleach.clean(
                html.unescape(new_comment.text), strip=True)
            new_comment.slug = defaultfilters.slugify(uuid.uuid4())
            new_comment.forum_post = post
            #new_comment.user_profile = self.request.user.profile.forumprofile
            new_comment.save()
            new_comment.slug = defaultfilters.slugify(post.slug + '_comment_' 
                               + str(new_comment.created_at or utils.timezone.now()))
            new_comment.save(update_fields=['slug'])
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
        pass
        return shortcuts.redirect(urls.reverse_lazy(self.a_name + ':post_view'))


class DeleteComment(mixins.LoginRequiredMixin, views.View):
    http_method_names = ['post']
    model = forum_models.ForumComment
    a_name = 'django_forum'

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        comment = self.model.objects.get(id=request.POST['comment-id'],
                                         slug=request.POST['comment-slug'])
        if comment.author == request.user:
            try:
                comment.delete()
            except self.model.DoesNotExist:
                logger.warn('the model you tried to delete does not exist')

        return shortcuts.redirect(comment)