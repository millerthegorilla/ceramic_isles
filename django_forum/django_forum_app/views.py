from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
from django_posts_and_comments.models import Post, Comment
from django_posts_and_comments.views import PostCreateView, PostListView, PostView
from django_posts_and_comments.forms import CommentForm
from django_profile.views import ProfileUpdateView
from django.forms.models import model_to_dict 
from .models import ProfileImage, ForumProfile, ForumPost
from .forms import  ForumPostCreateForm
### START LANDING PAGE

class LandingPageView(TemplateView):
    model = Post
    template_name = 'django_forum_app/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ProfileImage.objects.order_by('?')
        return context

### END LANDING PAGE



### START POSTS AND COMMENTS

class ForumPostView(PostView):
    model = ForumPost
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    template_name = 'django_forum_app/forum_post_detail.html'

    def post(self, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        comment_form = CommentForm(data=self.request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author_profile = self.request.user.profile.forumprofile
            new_comment.save()
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
    template_name = 'django_forum_app/forum_post_list.html'

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset()


class ForumPostCreateView(LoginRequiredMixin, PostCreateView):
    model = ForumPost
    template_name = "django_forum_app/forum_post_create_form.html"
    form_class = ForumPostCreateForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_profile = self.request.user.profile.forumprofile
        return super().form_valid(form, post)

### END POSTS AND COMMENTS