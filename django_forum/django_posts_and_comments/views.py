import bleach
import html
from uuid import uuid4
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.conf import settings
from django.db import IntegrityError
from .models import Post
from .forms import PostCreateForm

# Create your views here.


class PostView(DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
            """Return all published posts."""
            return self.model.objects.order_by('date_created')


class PostCreateView(CreateView):
    model = Post
    template_name_suffix = '_create_form'
    template_name = 'django_posts_and_comments/post_create_form.html'
    form_class = PostCreateForm

    def form_valid(self, form, **kwargs):
        breakpoint()
        post = form.save(commit=False)
        post.text = PostCreateView.sanitize_post_text(post.text)
        post.slug = slugify(post.title + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
        try:
            post.save()
        except IntegrityError as e:
            post.slug = slugify(post.title + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
            post.save()
        return redirect(self.success_url(post))

    def get_success_url(self, post, *args, **kwargs):
        return reverse_lazy('django_posts_and_comments:post_view', args=(post.id, post.slug,))

    @staticmethod
    def sanitize_post_text(text):
        return mark_safe(bleach.clean(html.unescape(text), 
                                           tags=settings.ALLOWED_TAGS, 
                                           attributes=settings.ATTRIBUTES, 
                                           styles=settings.STYLES, 
                                           strip=True, strip_comments=True))