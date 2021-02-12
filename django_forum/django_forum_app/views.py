from uuid import uuid4

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify

# Create your views here.
from django_posts_and_comments.models import Post, Comment
from django_posts_and_comments.views import PostCreateView, PostListView, PostView
from django_posts_and_comments.forms import CommentForm
from django_profile.views import ProfileUpdateView
from django.forms.models import model_to_dict 
from .models import ForumProfileImage, ForumProfile, ForumPost
from .forms import  ForumPostCreateForm

### START LANDING PAGE

class LandingPageView(TemplateView):
    model = ForumProfileImage
    template_name = 'django_forum_app/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ForumProfileImage.objects.filter(active=True).order_by('?')
        return context

### END LANDING PAGE



### START POSTS AND COMMENTS

class ForumPostView(PostView):
    model = ForumPost
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    template_name = 'django_forum_app/posts_and_comments/forum_post_detail.html'

    def post(self, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        comment_form = CommentForm(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user_profile = self.request.user.profile.forumprofile
            new_comment.save()
            return redirect(post)
        new_comment_form = CommentForm()
        return render(self.request, self.template_name, {'post': post,
                                                         'comment_form': new_comment_form})
    
    def get(self, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        new_comment_form = CommentForm()
        return render(self.request, self.template_name, {'post': post,
                                                         'comment_form': new_comment_form})


class ForumPostListView(LoginRequiredMixin, PostListView):
    model = ForumPost
    template_name = 'django_forum_app/posts_and_comments/forum_post_list.html'
    paginate_by = 6
    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset()



class ForumPostCreateView(LoginRequiredMixin, PostCreateView):
    model = ForumPost
    template_name = "django_forum_app/posts_and_comments/forum_post_create_form.html"
    form_class = ForumPostCreateForm

    def form_valid(self, form):
        breakpoint()
        post = form.save(commit=False)
        post.user_profile = self.request.user.profile.forumprofile
        post.text = PostCreateView.sanitize_post_text(post.text)
        post.slug = slugify(post.title) + str(uuid4())
        post.save()
        return redirect(self.get_success_url(post))

    def get_success_url(self, post, *args, **kwargs):
        return reverse_lazy('django_forum_app:post_view', args=(post.id, post.slug,))

## END POSTS AND COMMENTS