import bleach
import html
from uuid import uuid4
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.conf import settings
from .models import Post
from .forms import PostCreateForm

# Create your views here.


class PostView(DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'


class PostListView(ListView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    template_name_suffix = '_create_form'
    form_class = PostCreateForm

    def form_valid(self, form, post=None, **kwargs):
        if post is None:
            post = form.save(commit=False)

        post.text = mark_safe(bleach.clean(html.unescape(post.text), 
                                           tags=settings.ALLOWED_TAGS, 
                                           attributes=settings.ATTRIBUTES, 
                                           styles=settings.STYLES, 
                                           strip=True, strip_comments=True))
        post.slug = slugify(post.title) + str(uuid4())
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_view', args=(self.object.id, self.object.slug,))