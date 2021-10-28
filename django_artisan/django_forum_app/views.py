import bleach
import html
import logging
from uuid import uuid4
from elasticsearch_dsl import Q
from random import randint
from typing import Union

from django_q.tasks import schedule

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.http import JsonResponse, HttpResponseServerError
from django.forms.models import model_to_dict
from django.forms import ModelForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils import dateformat
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

# Create your views here.
from django_posts_and_comments.models import Post
from django_posts_and_comments.views import PostCreateView, PostListView, PostView
from django_profile.views import ProfileUpdateView
from django_users_app.views import RegisterView

from .documents import ForumPostDocument, ForumCommentDocument
from .models import ForumProfile, ForumPost, ForumComment
from .forms import ForumPostCreateForm, ForumPostListSearch, \
    ForumCommentForm, ForumProfileUserForm, \
    ForumProfileDetailForm
from .custom_registration_form import CustomUserCreationForm
from .models import create_user_forum_profile, Avatar, default_avatar
from .tasks import send_susbcribed_email
from typing import Any

logger = logging.getLogger('django')


# START POSTS AND COMMENTS
class ForumPostCreateView(PostCreateView):
    model = ForumPost
    template_name = "django_forum_app/posts_and_comments/forum_post_create_form.html"
    form_class = ForumPostCreateForm

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        post = form.save(commit=False)
        post.user_profile = self.request.user.profile.forumprofile
        post.text = PostCreateView.sanitize_post_text(post.text)
        post.slug = slugify(
            post.title[:60] + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
        post.save()
        if 'subscribe' in self.request.POST:
            post.subscribed_users.add(self.request.user)
        return redirect(self.get_success_url(post))

    def get_success_url(self, post: ForumPost, *args, **kwargs) -> str:
        return reverse_lazy(
            'django_forum_app:post_view', args=(
                post.id, post.slug,))


@method_decorator(never_cache, name='dispatch')
@method_decorator(never_cache, name='get')
class ForumPostView(PostView):
    """
        TODO: Replace superclass form processing if conditions with separate urls/views
              and overload them individually here, where necessary, instead of redefining
              the whole if clause.
    """
    model: ForumPost = ForumPost
    slug_url_kwarg: str = 'post_slug'
    slug_field: str = 'slug'
    template_name: str = 'django_forum_app/posts_and_comments/forum_post_detail.html'
    form_class: ForumPostCreateForm = ForumPostCreateForm
    comment_form_class: ForumCommentForm = ForumCommentForm
    #extra_context = { 'site_url':Site.objects.get_current().domain }

    def post(self, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        post = ForumPost.objects.get(pk=kwargs['pk'])
        if self.request.POST['type'] == 'post' and self.request.user.profile.display_name == post.author:
            post.delete()
            return redirect(reverse_lazy('django_forum_app:post_list_view'))
        elif self.request.POST['type'] == 'comment':
            comment_form = self.comment_form_class(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.text = bleach.clean(
                    html.unescape(new_comment.text), strip=True)
                new_comment.forum_post = post
                new_comment.user_profile = self.request.user.profile.forumprofile
                new_comment.save()
                schedule('django_forum_app.tasks.send_susbcribed_email',
                         name="subscribe_timeout" + str(uuid4()),
                         schedule_type="O",
                         repeats=-1,
                         next_run=timezone.now() + settings.COMMENT_WAIT,
                         post_id=post.id,
                         comment_id=new_comment.id,
                         path_info=self.request.path_info)
                return redirect(post)
            else:
                site = Site.objects.get_current()
                comments = ForumComment.objects.filter(post=post).all()
                return render(self.request,
                              self.template_name,
                              {'post': post,
                               'comments': comments,
                               'comment_form': comment_form,
                               'site_url': site.domain})
        elif self.request.POST['type'] == 'update':
            post.text = self.request.POST['update-post']
            post.category = self.request.POST['category']
            post.location = self.request.POST['location']
            post.save(update_fields=['text', 'location', 'category'])
            return redirect(post)
        elif self.request.POST['type'] == 'rem-comment':
            ForumComment.objects.get(pk=self.request.POST['comment']).delete()
            return redirect(post)
        elif self.request.POST['type'] == 'comment-update':
            try:
                comment = ForumComment.objects.get(id=self.request.POST['id'])
                comment.text = bleach.clean(html.unescape(
                    self.request.POST['comment-update']), strip=True)
                comment.save(update_fields=['text'])
                return redirect(post)
            except ObjectDoesNotExist as e:
                logger.error("Error accessing comment : {0}".format(e))
        elif self.request.POST['type'] == 'post-report':
            post.moderation = timezone.now()
            post.save(update_fields=['moderation'])
            ForumPostView.send_mod_mail('Post')
            return redirect(post)
        elif self.request.POST['type'] == 'comment-report':
            comment = ForumComment.objects.get(id=self.request.POST['id'])
            comment.moderation = timezone.now()
            comment.save(update_fields=['moderation'])
            ForumPostView.send_mod_mail('Comment')
            return redirect(post)
        else:
            return redirect('django_forum_app:post_list_view')

    @staticmethod
    def send_mod_mail(type: str) -> None:
        send_mail(
            'Moderation for {0}'.format(type),
            'A {0} has been created and requires moderation.  Please visit the {1} AdminPanel, and inspect the {0}'.format(
                type,
                settings.SITE_NAME),
            settings.EMAIL_HOST_USER,
            list(
                get_user_model().objects.filter(
                    is_staff=True).values_list(
                    'email',
                    flat=True)),
            fail_silently=False,
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        site = Site.objects.get_current()
        post = ForumPost.objects.get(pk=kwargs['pk'])
        form = self.form_class(user_name=self.request.user.username, post=post) # type: ignore
        subscribed = ''
        try:
            if post.subscribed_users.get(username=self.request.user.username): # type: ignore
                subscribed = 'checked'
        except get_user_model().DoesNotExist:
            subscribed = ''
        new_comment_form = self.comment_form_class() # type: ignore
        comments = ForumComment.objects.filter(post=post)
        user_display_name = self.request.user.profile.display_name
        category = post.get_category_display()
        cat_text = ''
        for i in [(cat.value, cat.label) for cat in settings.CATEGORY]:
            if i[1] == category:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'
        location = post.get_location_display()
        loc_text = ''
        for i in [(loc.value, loc.label) for loc in settings.LOCATION]:
            if i[1] == location:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'

        return render(self.request,
                      self.template_name,
                      {'form': form,
                       'post': post,
                       'category_opts': cat_text,
                       'location_opts': loc_text,
                       'subscribed': subscribed,
                       'comments': comments,
                       'comment_form': new_comment_form,
                       'user_display_name': user_display_name,
                       'site_url': (self.request.scheme or 'https') + '://' + site.domain})


def subscribe(request) -> JsonResponse:
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        try:
            fp = ForumPost.objects.get(slug=request.POST['post_slug'])
            if request.POST['data'] == 'true':
                fp.subscribed_users.add(request.user)
            else:
                fp.subscribed_users.remove(request.user)
            return JsonResponse({}, status=200)
        except ForumPost.DoesNotExist as e:
            logger.error('There is no post with that slug : {0}'.format(e))
            return JsonResponse(
                {"error": "no post with that slug"}, 
                status=500)
    else:
        return JsonResponse(
            {"error": ""}, 
            status=500)


@method_decorator(never_cache, name='dispatch')
class ForumPostListView(PostListView):
    model = ForumPost
    template_name = 'django_forum_app/posts_and_comments/forum_post_list.html'
    paginate_by = 5
    """
       the documentation for django-elasticsearch and elasticsearch-py as well as elasticsearch
       is not particularly good, at least not in my experience.  The following searches posts and
       comments.  The search indexes are defined in documents.py.
    """

    def get(self, request: HttpRequest, search_slug: str = None) -> HttpResponse:
        breakpoint()
        site = Site.objects.get_current()
        search = 0
        p_c = None
        is_a_search = False
        if search_slug == 'search':
            is_a_search = True
            form = ForumPostListSearch(request.GET)
            breakpoint()
            if form.is_valid():
                terms = form.cleaned_data['q'].split(' ')
                if len(terms) > 1:
                    t = 'terms'
                else:
                    t = 'match'
                    terms = terms[0]
                queryset_p = ForumPostDocument.search().query(
                    Q(t, text=terms) |
                    Q(t, author=terms) |
                    Q(t, title=terms) |
                    Q(t, category=terms) |
                    Q(t, location=terms)).to_queryset()
                queryset_c = ForumCommentDocument.search().query(
                    Q(t, text=terms) | Q(t, author=terms)).to_queryset()
                p_c = list(queryset_p) + list(queryset_c)
                search = len(p_c)
                if search == 0:
                    queryset = ForumPost.objects.all()
            else:
                # TODO: show form errors?
                return render(request, self.template_name, {'form': form})
        else:
            queryset = ForumPost.objects.order_by('-pinned')
        if search:
            paginator = Paginator(p_c, self.paginate_by)
        else:
            paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'search': search,
            'is_a_search': is_a_search,
            'site_url': request.scheme + '://' + site.domain}
        return render(request, self.template_name, context)

## autocomplete now removed to reduce number of requests
# def autocomplete(request):
#     max_items = 5
#     q = request.GET.get('q')
#     results = []
#     if q:
#         search = ForumPostDocument.search().suggest('results', q, term={'field':'text'})
#         result = search.execute()
#         for idx,item in enumerate(result.suggest['results'][0]['options']):
#             results.append(item.text)
#     return JsonResponse({
#         'results': results
#     })

# END POSTS AND COMMENTS


# START PROFILE
@method_decorator(never_cache, name='dispatch')
class ForumProfileUpdateView(ProfileUpdateView):
    model = ForumProfile
    form_class = ForumProfileDetailForm
    user_form_class = ForumProfileUserForm
    success_url = reverse_lazy('django_forum_app:profile_update_view')
    template_name = 'django_forum_app/profile/forum_profile_update_form.html'

    def form_valid(self, form: ModelForm, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        if self.request.POST['type'] == 'update-profile':
            if form.has_changed():
                form.save()
            return super().form_valid(form)  # process other form in django_profile app
        elif self.request.POST['type'] == 'update-avatar':
            fp = ForumProfile.objects.get(profile_user=self.request.user)
            fp.avatar.image_file.save(
                self.request.FILES['avatar'].name,
                self.request.FILES['avatar'])
            return redirect(self.success_url)

    def get_context_data(self, **args) -> dict:
        context = super().get_context_data(**args)
        context['avatar'] = ForumProfile.objects.get(
            profile_user=self.request.user).avatar
        queryset = ForumPost.objects.filter(
            author=self.request.user.profile.display_name)
        paginator = Paginator(queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
# END PROFILE

# NEEDED FOR ADDITION OF DISPLAY_NAME AND FORUM RULES
# the following goes in the project top level urls.py
# from django_forum_app.views import CustomRegisterView
# path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),


class CustomRegisterView(RegisterView):
    form_class = CustomUserCreationForm

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponseRedirect:
        user = form.save()
        user.profile.forumprofile.rules_agreed = form['rules'].value()
        user.profile.forumprofile.save(update_fields=['rules_agreed'])
        user.profile.display_name = slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        user.save()
        super().form_valid(form, user)
        return redirect('password_reset_done')


class RulesPageView(TemplateView):
    template_name = 'django_forum_app/rules.html'
    extra_context = {'app_name': settings.SITE_NAME}
