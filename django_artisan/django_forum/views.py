import bleach, html, logging, uuid, elasticsearch_dsl, typing

from django_q import tasks

from django import urls, forms, shortcuts, http, utils, conf
from django.template import defaultfilters
from django.core import exceptions, mail
from django.contrib import auth
from django.views.decorators import cache

from django.views import generic
from django.contrib.sites import models as site_models

# Create your views here.
from django_posts_and_comments import views as posts_and_comments_views
from django_profile import views as profile_views
from django_users import views as users_views

from . import documents as forum_documents
from . import models as forum_models
from . import forms as forum_forms
from . import custom_registration as custom_reg_form

logger = logging.getLogger('django_artisan')


# START POSTS AND COMMENTS
class ForumPost(posts_and_comments_views.Post):
    model = forum_models.ForumPost
    template_name = "django_forum/posts_and_comments/forum_post_create_form.html"
    form_class = forum_forms.ForumPost

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        post = form.save(commit=False)
        post.user_profile = self.request.user.profile.forumprofile
        post.text = posts_and_comments_views.Post.sanitize_post_text(post.text)
        post.slug = defaultfilters.slugify(
            post.title[:60] + '-' + str(utils.dateformat.format(utils.timezone.now(), 'Y-m-d H:i:s')))
        post.save()
        if 'subscribe' in self.request.POST:
            post.subscribed_users.add(self.request.user)
        return shortcuts.redirect(self.get_success_url(post))

    def get_success_url(self, post: forum_models.ForumPost, *args, **kwargs) -> str:
        return urls.reverse_lazy(
            'django_forum:post_view', args=(
                post.id, post.slug,))


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
@utils.decorators.method_decorator(cache.never_cache, name='get')
class ForumPostView(posts_and_comments_views.Post):
    """
        TODO: Replace superclass form processing if conditions with separate urls/views
              and overload them individually here, where necessary, instead of redefining
              the whole if clause.
    """
    model: forum_models.ForumPost = forum_models.ForumPost
    slug_url_kwarg: str = 'post_slug'
    slug_field: str = 'slug'
    template_name: str = 'django_forum/posts_and_comments/forum_post_detail.html'
    form_class: forum_forms.ForumPost = forum_forms.ForumPost
    comment_form_class: forum_forms.ForumComment = forum_forms.ForumComment
    #extra_context = { 'site_url':Site.objects.get_current().domain }

    def post(self, *args, **kwargs) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]:
        post = forum_models.ForumPost.objects.get(pk=kwargs['pk'])
        if self.request.POST['type'] == 'post' and self.request.user.profile.display_name == post.author:
            post.delete()
            return shortcuts.redirect(urls.reverse_lazy('django_forum:post_list_view'))
        elif self.request.POST['type'] == 'comment':
            comment_form = self.comment_form_class(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.text = bleach.clean(
                    html.unescape(new_comment.text), strip=True)
                new_comment.forum_post = post
                new_comment.user_profile = self.request.user.profile.forumprofile
                new_comment.save()
                tasks.schedule('django_forum.tasks.send_susbcribed_email',
                             name="subscribe_timeout" + str(uuid.uuid4()),
                             schedule_type="O",
                             repeats=-1,
                             next_run=utils.timezone.now() + conf.settings.COMMENT_WAIT,
                             post_id=post.id,
                             comment_id=new_comment.id,
                             path_info=self.request.path_info)
                return shortcuts.redirect(post)
            else:
                site = site_models.Site.objects.get_current()
                comments = forum_models.ForumComment.objects.filter(post=post).all()
                return shortcuts.render(self.request,
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
            return shortcuts.redirect(post)
        elif self.request.POST['type'] == 'rem-comment':
            forum_models.ForumComment.objects.get(pk=self.request.POST['comment']).delete()
            return shortcuts.redirect(post)
        elif self.request.POST['type'] == 'comment-update':
            try:
                comment = forum_models.ForumComment.objects.get(id=self.request.POST['id'])
                comment.text = bleach.clean(html.unescape(
                    self.request.POST['comment-update']), strip=True)
                comment.save(update_fields=['text'])
                return shortcuts.redirect(post)
            except exceptions.ObjectDoesNotExist as e:
                logger.error("Error accessing comment : {0}".format(e))
                return http.HttpResponse(status=500)
        elif self.request.POST['type'] == 'post-report':
            post.moderation = utils.timezone.now()
            post.save(update_fields=['moderation'])
            ForumPostView.send_mod_mail('Post')
            return shortcuts.redirect(post)
        elif self.request.POST['type'] == 'comment-report':
            comment = forum_models.ForumComment.objects.get(id=self.request.POST['id'])
            comment.moderation = utils.timezone.now()
            comment.save(update_fields=['moderation'])
            ForumPostView.send_mod_mail('Comment')
            return shortcuts.redirect(post)
        else:
            return shortcuts.redirect('django_forum:post_list_view')

    @staticmethod
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

    def get(self, *args, **kwargs) -> http.HttpResponse:
        site = site_models.Site.objects.get_current()
        post = forum_models.ForumPost.objects.get(pk=kwargs['pk'])
        form = self.form_class(user_name=self.request.user.username, post=post) # type: ignore
        subscribed = ''
        try:
            if post.subscribed_users.get(username=self.request.user.username): # type: ignore
                subscribed = 'checked'
        except auth.get_user_model().DoesNotExist:
            subscribed = ''
        new_comment_form = self.comment_form_class() # type: ignore
        comments = forum_models.ForumComment.objects.filter(post=post)
        user_display_name = self.request.user.profile.display_name
        category = post.get_category_display()
        cat_text = ''
        for i in [(cat.value, cat.label) for cat in conf.settings.CATEGORY]:
            if i[1] == category:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                cat_text = cat_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'
        location = post.get_location_display()
        loc_text = ''
        for i in [(loc.value, loc.label) for loc in conf.settings.LOCATION]:
            if i[1] == location:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '" selected>' + str(i[1]) + '</option>'
            else:
                loc_text = loc_text + '<option value="' + \
                    str(i[0]) + '">' + str(i[1]) + '</option>'

        return shortcuts.render(self.request,
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


def subscribe(request) -> http.JsonResponse:
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        try:
            fp = forum_models.ForumPost.objects.get(slug=request.POST['post_slug'])
            if request.POST['data'] == 'true':
                fp.subscribed_users.add(request.user)
            else:
                fp.subscribed_users.remove(request.user)
            return http.JsonResponse({}, status=200)
        except forum_models.ForumPost.DoesNotExist as e:
            logger.error('There is no post with that slug : {0}'.format(e))
            return http.JsonResponse(
                {"error": "no post with that slug"}, 
                status=500)
    else:
        return http.JsonResponse(
            {"error": ""}, 
            status=500)


@utils.decorators.method_decorator(cache.never_cache, name='dispatch')
class ForumPostList(posts_and_comments_views.PostList):
    model = forum_models.ForumPost
    template_name = 'django_forum/posts_and_comments/forum_post_list.html'
    paginate_by = 5
    """
       the documentation for django-elasticsearch and elasticsearch-py as well as elasticsearch
       is not particularly good, at least not in my experience.  The following searches posts and
       comments.  The search indexes are defined in documents.py.
    """

    def get(self, request: http.HttpRequest, search_slug: str = None) -> http.HttpResponse: # type: ignore
        '''
            I had a function that tested for the existence of a search slug
            and then performed the search if necessary.  I have refactored that
            to the below, that uses duck typing (type coercion) to performs the 
            logic to the search.  It is probably a lot slower, but seems more pythonic.
            So, TODO profile this method vs the original from commit id
            1d5cbccde9f7b183e4d886d7e644712b79db60cd 
        '''
        site = site_models.Site.objects.get_current()
        search = 0
        p_c = None
        is_a_search = False
        form = forum_forms.ForumPostListSearch(request.GET)
        if form.is_valid():
            is_a_search = True
            terms = form.cleaned_data['q'].split(' ')
            if len(terms) > 1:
                t = 'terms'
            else:
                t = 'match'
                terms = terms[0]
            queryset_p = forum_documents.ForumPost.search().query(
                elasticsearch_dsl.Q(t, text=terms) |
                elasticsearch_dsl.Q(t, author=terms) |
                elasticsearch_dsl.Q(t, title=terms) |
                elasticsearch_dsl.Q(t, category=terms) |
                elasticsearch_dsl.Q(t, location=terms)).to_queryset()
            queryset_c = forum_documents.ForumComment.search().query(
                elasticsearch_dsl.Q(t, text=terms) | elasticsearch_dsl.Q(t, author=terms)).to_queryset()
            p_c = list(queryset_p) + list(queryset_c)
            search = len(p_c)
            if search == 0:
                queryset = forum_models.ForumPost.objects.order_by('-pinned')
                paginator = paginator.Paginator(queryset, self.paginate_by)
            else:
                paginator = paginator.Paginator(p_c, self.paginate_by)
        else:
            queryset = forum_models.ForumPost.objects.order_by('-pinned')
            paginator = paginator.Paginator(queryset, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'search': search,
            'is_a_search': is_a_search,
            'site_url': (request.scheme or 'https') + '://' + site.domain}
        return shortcuts.render(request, self.template_name, context)
            # # TODO: show form errors?
            # breakpoint()
            # return shortcuts.render(request, self.template_name, {'form': form, 'is_a_search': False })

## autocomplete now removed to reduce number of requests
# def autocomplete(request):
#     max_items = 5
#     q = request.GET.get('q')
#     results = []
#     if q:
#         search = ForumPost.search().suggest('results', q, term={'field':'text'})
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
    form_class = forum_forms.ForumProfile
    user_form_class = forum_forms.ForumProfileUser
    success_url = urls.reverse_lazy('django_forum:profile_update_view')
    template_name = 'django_forum/profile/forum_profile_update_form.html'

    def form_valid(self, form: forms.ModelForm) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: # type: ignore
    # mypy can't handle inheritance properly, and grumbles about a missing return statement
        if self.request.POST['type'] == 'update-profile':
            if form.has_changed():
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
        context['avatar'] = forum_models.ForumProfile.objects.get(
            profile_user=self.request.user).avatar
        queryset = forum_models.ForumPost.objects.filter(
            author=self.request.user.profile.display_name)
        paginator = paginator.Paginator(queryset, 6)
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
        user.profile.forumprofile.rules_agreed = form['rules'].value()
        user.profile.forumprofile.save(update_fields=['rules_agreed'])
        user.profile.display_name = defaultfilters.slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        user.save()
        super().form_valid(form, user)
        return shortcuts.redirect('password_reset_done')


class RulesPageView(generic.base.TemplateView):
    template_name = 'django_forum/rules.html'
    extra_context = {'app_name': conf.settings.SITE_NAME}
