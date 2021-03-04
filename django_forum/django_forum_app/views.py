from uuid import uuid4
import bleach
import html
from elasticsearch_dsl import Q

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.http import JsonResponse, HttpResponseServerError
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils import dateformat
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.conf import settings

# Create your views here.
from django_posts_and_comments.models import Post
from django_posts_and_comments.views import PostCreateView, PostListView, PostView
from django_profile.views import ProfileUpdateView
from django_users_app.views import RegisterView

from .documents import ForumPostDocument, ForumCommentDocument
from .models import ForumProfileImage, ForumProfile, ForumPost, ForumComment, Event
from .forms import  ForumPostCreateForm, ForumPostListSearch, ForumCommentForm
from .custom_forms import CustomUserCreationForm
### START LANDING PAGE

class LandingPageView(TemplateView):
    model = ForumProfileImage
    template_name = 'django_forum_app/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ForumProfileImage.objects.filter(active=True).order_by('?')
        context['image_size'] = "1024x768"
        context['username'] = self.request.user.username
        return context

### END LANDING PAGE



### START POSTS AND COMMENTS
@method_decorator(never_cache, name='dispatch')
@method_decorator(never_cache, name='get')
class ForumPostView(LoginRequiredMixin, PostView):
    model = ForumPost
    slug_url_kwarg = 'post_slug'
    slug_field = 'slug'
    template_name = 'django_forum_app/posts_and_comments/forum_post_detail.html'
    form_class = ForumCommentForm

    def post(self, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        if self.request.POST['type'] == 'post' and self.request.user.username == post.author:
            post.delete()
            return redirect(reverse_lazy('django_forum_app:post_list_view'))
        elif self.request.POST['type'] == 'comment':
            comment_form = self.form_class(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.text = bleach.clean(html.unescape(new_comment.text), strip=True)
                new_comment.forum_post = post
                new_comment.user_profile = self.request.user.profile.forumprofile
                new_comment.save()
                return redirect(post)
            else:
                comments = ForumComment.objects.filter(post=post).all()
                return render(self.request, self.template_name, {'post': post,
                                                             'comments': comments,
                                                             'comment_form': comment_form})
        elif self.request.POST['type'] == 'update':
            post.text = self.request.POST['update-post']
            post.save(update_fields=['text'])
            return redirect(post)
        elif self.request.POST['type'] == 'rem-comment':
            ForumComment.objects.get(pk=self.request.POST['comment']).delete()
            return redirect(post)
        elif self.request.POST['type'] == 'comment-update':
            try:
                comment = ForumComment.objects.get(id=self.request.POST['id'])
                comment.text = bleach.clean(html.unescape(self.request.POST['comment-update']), strip=True)
                comment.save(update_fields=['text'])
                return redirect(post)
            except ObjectDoesNotExist as e:
                pass  ### TODO: log errors here.
        elif self.request.POST['type'] == 'post-report':
            post.moderation = timezone.now()
            post.save(update_fields=['moderation'])
            return redirect(post)
        elif self.request.POST['type'] == 'comment-report':
            comment = ForumComment.objects.get(id=self.request.POST['id'])
            comment.moderation = timezone.now()
            comment.save(update_fields=['moderation'])
            return redirect(post)
        else:
            return HttpResponseServerError()

    def get(self, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        new_comment_form = self.form_class()
        comments = ForumComment.objects.filter(post=post)
        return render(self.request, self.template_name, {'post': post,
                                                         'comments': comments,
                                                         'comment_form': new_comment_form})


@method_decorator(never_cache, name='dispatch')
class ForumPostListView(LoginRequiredMixin, PostListView):
    model = ForumPost
    template_name = 'django_forum_app/posts_and_comments/forum_post_list.html'
    paginate_by = 6
 
    def get(self, request, search_slug=None):
        search = 0
        p_c = None
        is_a_search = False
        if search_slug == 'search':
            is_a_search = True
            form = ForumPostListSearch(request.GET)
            if form.is_valid():
                terms = form.cleaned_data['q'].split(' ')
                if len(terms) > 1:
                    t = 'terms'
                else:
                    t = 'term'
                    terms = terms[0]
                queryset_p = ForumPostDocument.search().query(
                            Q(t, text=terms)|
                            Q(t, author=terms)|
                            Q(t, title=terms) |
                            Q(t, category=terms)).to_queryset()
                queryset_c = ForumCommentDocument.search().query(Q(t, text=terms)|Q(t, author=terms)).to_queryset()
                p_c = list(queryset_p) + list(queryset_c)
                search = len(p_c)
                if search == 0: 
                    queryset = ForumPost.objects.all()
            else:
                return render(request, self.template_name, {'form':form})  ## TODO: show form errors?
        else:
            queryset = ForumPost.objects.all()
        if search:
            paginator = Paginator(p_c, 6)
        else:
            paginator = Paginator(queryset, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = { 'page_obj': page_obj, 'search': search, 'is_a_search': is_a_search}
        return render(request, self.template_name, context)
   

class PersonalPageView(DetailView):
    model = ForumProfile
    slug_url_kwarg = 'name_slug'
    slug_field = 'display_name'
    template_name = 'django_forum_app/personal_page.html'

    def get_queryset(self):  #TODO: try/except clause
        return ForumProfile.objects.filter(display_name=self.request.resolver_match.kwargs['name_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ForumProfileImage.objects.filter(
                                user_profile=self.object).filter(active=True).order_by('?')
        u_p = self.get_queryset().first()
        context['profile_image_file'] = u_p.image_file
        if context['profile_image_file'].name == '':
            context['profile_image_file'] = None
        context['name'] = u_p.profile_user.first_name + " " + u_p.profile_user.last_name
        if context['name'] == ' ':
            context['name'] = None
        context['display_name'] = u_p.display_name
        context['bio'] = u_p.bio
        context['image_size'] = "1024x768"
        context['shop_link'] = u_p.shop_web_address
        context['outlets'] = u_p.outlets
        return context

# def posts_search(request):
#     form = ForumPostListSearch(request.GET)

#     context = {}
#     if form.is_valid():
#         qset = search.filter(Q('nested', 
#             path='forum_comments', 
#             query=Q('terms', 
#                 forum_comments__text=form.cleaned_data['q'].split[' ']))).filter(Q('terms', 
#                                 text=form.cleaned_date['q'].split[' '])).to_queryset()

#         # if qset.count() > 0:
#         #     context['forum_post_list'] = qset
#         #     context['page_obj'] =         
#         # page_number = request.GET.get('page')
#         # results = SearchQuerySet().filter(content=AutoQuery(form.cleaned_data['q']))
#         # context['page'] = Paginator(results, settings.SEARCH_RESULTS_PER_PAGE).get_page(page_number)

#     context['form'] = form

#     return render(request, 'django_forum_app/posts_and_comments/forum_post_list.html', context)


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


class ForumPostCreateView(LoginRequiredMixin, PostCreateView):
    model = ForumPost
    template_name = "django_forum_app/posts_and_comments/forum_post_create_form.html"
    form_class = ForumPostCreateForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_profile = self.request.user.profile.forumprofile
        post.text = PostCreateView.sanitize_post_text(post.text)
        post.slug = slugify(post.title + '-' + str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')))
        post.save()
        return redirect(self.get_success_url(post))
 
    def get_success_url(self, post, *args, **kwargs):
        return reverse_lazy('django_forum_app:post_view', args=(post.id, post.slug,))

## END POSTS AND COMMENTS

class AboutPageView(ListView):
    model = Event
    template_name = 'django_forum_app/about.html'
    
    def get_context_data(self):
        data = super().get_context_data()
        data['about_text'] = settings.ABOUT_US_SPIEL
        qs = ForumProfile.objects.all().exclude(profile_user__is_superuser=True) \
                                       .values_list('display_name', flat=True)
        data['dnames'] = qs
        data['colours'] = ['text-white', 'text-purple', 'text-warning', 'text-lightgreen', 'text-danger', 'headline-text', 'sub-headline-text']
        return data

    def get_queryset(self):
            """Return all published posts."""
             # filter objects created today
            qs_bydate = self.model.objects.filter(time__gt=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
            qs_repeating = self.model.objects.filter(repeating=True)
            return qs_bydate | qs_repeating


# class PeopleDirectoryView(TemplateView):
#     template_name = 'django_forum_app/people.html'

#     def get_context_data(self):
#         """ couldn't get the values() to pass back an appropriate queryset, and since
#              this view does not require loginrequiredmixin, perhaps a list of names is 
#              safer? """
#         uname_list = []
#         data = {}
#         qs = ForumProfile.objects.all().exclude(profile_user__is_superuser=True) \
#                                        .values_list('display_name', flat=True)
#         data['dnames'] = qs
#         data['colours'] = ['text-white', 'text-purple', 'text-warning', 'text-lightgreen', 'text-danger', 'headline-text', 'sub-headline-text']
#         return data

class CustomRegisterView(RegisterView):
    form_class = CustomUserCreationForm
    
    def form_valid(self, form):
        user = form.save()
        user.profile.display_name = slugify(form['display_name'].value())
        user.profile.rules_agreed = form['rules'].value()
        user.profile.save(update_fields=['display_name','rules_agreed'])
        super().form_valid(form, user)
        #send_email(user, custom_salt=uuid.uuid4())
        return redirect('password_reset_done')