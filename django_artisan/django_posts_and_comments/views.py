import bleach
import html
import logging
from uuid import uuid4

from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils import dateformat
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Post, Comment
from .forms import PostCreateForm, CommentForm
from typing import Any


logger = logging.getLogger('django')


@method_decorator(never_cache, name='dispatch')
@method_decorator(never_cache, name='get')
class PostView(LoginRequiredMixin, DetailView):
    """
        TODO: replace the single view/many form processing with separate urls for
              each form action, pointing to individual views, each with its own form class,
              each redirecting to this url/view with its get_context_data, for all forms.
    """
    model = Post
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    template_name = 'django_posts_and_comments/post_detail.html'
    form_class = CommentForm

    def post(self, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if self.request.POST['type'] == 'post' and self.request.user.profile.display_name == post.post_author(
        ):
            post.delete()
            return redirect(
                reverse_lazy('django_posts_and_comments:post_list_view'))
        elif self.request.POST['type'] == 'comment':
            comment_form = self.form_class(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.text = bleach.clean(
                    html.unescape(new_comment.text), strip=True)
                new_comment.post = post
                new_comment.user_profile = self.request.user.profile
                new_comment.save()
                return redirect(post)
            else:
                comments = Comment.objects.filter(post=post).all()
                return render(
                    self.request, self.template_name, {
                        'post': post, 'comments': comments, 'comment_form': comment_form})
        elif self.request.POST['type'] == 'update':
            post.text = self.request.POST['update-post']
            post.save(update_fields=['text'])
            return redirect(post)
        elif self.request.POST['type'] == 'rem-comment':
            Comment.objects.get(pk=self.request.POST['comment']).delete()
            return redirect(post)
        elif self.request.POST['type'] == 'comment-update':
            try:
                comment = Comment.objects.get(id=self.request.POST['id'])
                comment.text = bleach.clean(html.unescape(
                    self.request.POST['comment-update']), strip=True)
                comment.save(update_fields=['text'])
                return redirect(post)
            except ObjectDoesNotExist as e:
                logger.error("Error accessing comment : {0}".format(e))
        else:
            logger.warn("request has no processable type")
            return redirect('django_posts_and_comments:post_list_view')

    def get(self, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        new_comment_form = self.form_class()
        comments = Comment.objects.filter(post=post)
        user_display_name = self.request.user.profile.display_name
        return render(self.request,
                      self.template_name,
                      {'post': post,
                       'comments': comments,
                       'comment_form': new_comment_form,
                       'user_display_name': user_display_name})


@method_decorator(never_cache, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'django_posts_and_comments/post_list.html'
    paginate_by = 6

    def get(self, request):
        queryset = Post.objects.all()
        paginator = Paginator(queryset, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name_suffix = '_create_form'
    template_name = 'django_posts_and_comments/post_create_form.html'
    form_class = PostCreateForm

    def form_valid(self, form, **kwargs) -> Any:
        post = form.save(commit=False)
        post.text = PostCreateView.sanitize_post_text(post.text)
        post.user_profile = self.request.user.profile
        post.slug = slugify(
            post.title + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
        try:
            post.save()
        except IntegrityError as e:
            post.slug = slugify(
                post.title + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
            post.save()
        return redirect(self.get_success_url(post))

    def get_success_url(self, post, *args, **kwargs) -> Any:
        return reverse_lazy(
            'django_posts_and_comments:post_view', args=(
                post.id, post.slug,))

    @staticmethod
    def sanitize_post_text(text) -> Any:
        return mark_safe(bleach.clean(html.unescape(text),
                                      tags=settings.ALLOWED_TAGS,
                                      attributes=settings.ATTRIBUTES,
                                      styles=settings.STYLES,
                                      strip=True, strip_comments=True))
