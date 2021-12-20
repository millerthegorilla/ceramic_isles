import bleach, html, logging, uuid, elasticsearch_dsl, typing

from django_q import tasks

from django import urls, forms, shortcuts, http, utils, conf
from django.core import exceptions, mail, paginator as pagination
from django.contrib import auth
from django.contrib.auth import mixins
from django.contrib.sites import models as site_models
from django.db import models as db_models
from django.template import defaultfilters
from django.views.decorators import cache
from django.views import generic

# Create your views here.
from django_messages import views as messages_views
from django_profile import views as profile_views
from django_users import views as users_views

from . import documents as forum_documents
from . import models as forum_models
from . import forms as forum_forms
from . import forms_custom_registration as custom_reg_form

logger = logging.getLogger('django_artisan')


# START POSTS AND COMMENTS
class PostCreate(mixins.LoginRequiredMixin, messages_views.MessageCreate):
    model = forum_models.Post
    template_name = "django_forum/posts_and_comments/forum_post_create_form.html"
    form_class = forum_forms.Post

    def form_valid(self, form: forum_forms.Post, post: forum_models.Post) -> http.HttpResponseRedirect:
        if post is None:
            post = form.save(commit=False)
        post = super().form_valid(form, post)
        if 'subscribe' in self.request.POST:
            post.subscribed_users.add(self.request.user)
        return shortcuts.redirect(self.get_success_url(post))

    def get_success_url(self, post: forum_models.Post, *args, **kwargs) -> str:
        return urls.reverse_lazy(
            'django_forum:post_view', args=(
                post.id, post.slug,))


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
class PostList(mixins.LoginRequiredMixin, messages_views.MessageList):
    model = forum_models.Post
    template_name = 'django_forum/posts_and_comments/forum_post_list.html'
    paginate_by = 5
    """
       the documentation for django-elasticsearch and elasticsearch-py as well as elasticsearch
       is not particularly good, at least not in my experience.  The following searches posts and
       comments.  The search indexes are defined in documents.py.
    """

    def get(self, request: http.HttpRequest) -> typing.Union[tuple, http.HttpResponse]:
        '''
            I had a function that tested for the existence of a search slug
            and then performed the search if necessary.  I have refactored that
            to the below, that uses duck typing (type coercion) to perform the 
            logic of the search.  It is probably a lot slower, but seems more pythonic.
            So, TODO profile this method vs the original from commit id
            1d5cbccde9f7b183e4d886d7e644712b79db60cd 
        '''
        def get(self, request: http.HttpRequest) -> typing.Union[tuple, http.HttpResponse]:
            site = site_models.Site.objects.get_current()
            search = 0
            p_c = None
            is_a_search = False
            form = artisan_forms.PostListSearch(request.GET)
            if form.is_valid():
                is_a_search = True
                terms = form.cleaned_data['q'].split(' ')
                if len(terms) > 1:
                    t = 'terms'
                else:
                    t = 'match'
                    terms = terms[0]
                queryset = forum_documents.Post.search().query(
                    elasticsearch_dsl.Q(t, text=terms) |
                    elasticsearch_dsl.Q(t, author=terms) |
                    elasticsearch_dsl.Q(t, title=terms) |
                    elasticsearch_dsl.Q(t, category=terms) |
                    elasticsearch_dsl.Q(t, location=terms)).to_queryset()
                time_range = eval('form.' + form['published'].value())  #### TODO !!! eval is evil.  
                search = len(queryset)
                if search and time_range:
                    queryset = queryset.filter(created_at__lt=time_range[0], created_at__gt=time_range[1])
                    search = len(queryset)
                if not search:
                    queryset = forum_models.Post.objects.order_by('-pinned')
            else:
                form.errors.clear()
                queryset = forum_models.Post.objects.order_by('-pinned')
             
            paginator = pagination.Paginator(queryset, self.paginate_by)
             
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                'form': form,
                'page_obj': page_obj,
                'search': search,
                'is_a_search': is_a_search,
                'site_url': (request.scheme or 'https') + '://' + site.domain}
            return shortcuts.render(request, self.template_name, context)

## autocomplete now removed to reduce number of requests
# def autocomplete(request):
#     max_items = 5
#     q = request.GET.get('q')
#     results = []
#     if q:
#         search = Post.search().suggest('results', q, term={'field':'text'})
#         result = search.execute()
#         for idx,item in enumerate(result.suggest['results'][0]['options']):
#             results.append(item.text)
#     return JsonResponse({
#         'results': results
#     })

# END POSTS AND COMMENTS


# START PROFILE
@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
class ForumProfile(profile_views.ProfileUpdate):
    model = forum_models.ForumProfile
    post_model = forum_models.Post
    form_class = forum_forms.ForumProfile
    user_form_class = forum_forms.ForumProfileUser
    success_url = urls.reverse_lazy('django_forum:profile_update_view')
    template_name = 'django_forum/profile/forum_profile_update_form.html'

    def form_valid(self, form: forms.ModelForm) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: # type: ignore
    # mypy can't handle inheritance properly, and grumbles about a missing return statement
        if self.request.POST['type'] == 'update-profile':
            user_form = self.user_form_class(self.request.POST)
            if form.has_changed() or user_form.has_changed():
                obj = form.save(commit=False)
                if user_form.has_changed():  ## horridly hacky
                    obj.display_name = defaultfilters.slugify(user_form['display_name'].value())
                obj.save()
                form.save()
            return super().form_valid(form)  # process other form in django_profile app
        elif self.request.POST['type'] == 'update-avatar':
            fp = forum_models.ForumProfile.objects.get(profile_user=self.request.user)
            fp.avatar.image_file.save(
                self.request.FILES['avatar'].name,
                self.request.FILES['avatar'])
            return shortcuts.redirect(self.success_url)

    def get_context_data(self, **args) -> dict:
        context = super().get_context_data(**args)
        context['avatar'] = self.model.objects.get(
            profile_user=self.request.user).avatar
        queryset = (self.post_model.objects.select_related('author')
                               .select_related('author__profile')
                               .filter(author=self.request.user))
        paginator = pagination.Paginator(queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
# END PROFILE

# NEEDED FOR ADDITION OF DISPLAY_NAME AND FORUM RULES
# the following goes in the project top level urls.py
# from django_forum.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),


class CustomRegister(users_views.Register):
    form_class = custom_reg_form.CustomUserCreation

    def form_valid(self, form: custom_reg_form.CustomUserCreation) -> http.HttpResponseRedirect:
        user = form.save()
        user.profile.rules_agreed = form['rules'].value()
        user.profile.save(update_fields=['rules_agreed'])
        user.profile.display_name = defaultfilters.slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        user.save() ## TODO do I need this save?
        super().form_valid(form, user)
        return shortcuts.redirect('password_reset_done')


class RulesPageView(generic.base.TemplateView):
    template_name = 'django_forum/rules.html'
    extra_context = {'app_name': conf.settings.SITE_NAME}
