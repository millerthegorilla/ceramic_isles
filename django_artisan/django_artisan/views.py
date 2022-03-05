import random, logging, elasticsearch_dsl, typing, json, PIL
from PIL import Image, ImageOps
from sorl.thumbnail import get_thumbnail

from django_q import tasks

from django import conf, http, forms, shortcuts, urls, utils
from django.core import paginator as pagination
from django.core import serializers
from django.contrib.auth import mixins
from django.contrib import sitemaps
from django.contrib.sites import models as site_models
from django.db import models as db_models
from django.middleware import csrf
from django.utils import decorators
from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators import cache

from django_forum import forms as forum_forms
from django_forum import views as forum_views
from django_forum import models as forum_models

from . import models as artisan_models
from . import forms as artisan_forms
from . import documents as artisan_documents 

logger = logging.getLogger('django_artisan')

# TODO enable cache and bust it when new post is created.
@decorators.method_decorator(cache.never_cache, name='dispatch')
class PostList(forum_views.PostList):
    model = artisan_models.Post
    template_name = 'django_forum/posts_and_comments/forum_post_list.html'
    paginate_by = 5

    def get(self, request: http.HttpRequest) -> typing.Union[tuple, http.HttpResponse]:
        #  site_models is really slow. so I use settings object instead
        #  site = site_models.Site.objects.get_current()
        search = 0
        p_c = None
        is_a_search = False
        form = artisan_forms.PostListSearch(request.GET)
        if form.is_valid(): ## could make a search object factory class to hide implementation of search,
            is_a_search = True   ##  to allow search method (elasticsearch, postgres full text etc) to be changed
            terms = form.cleaned_data['q'].split(' ')
            if len(terms) > 1:
                t = 'terms'
            else:
                t = 'match'
                terms = terms[0]
            queryset = artisan_documents.Post.search().query(
                elasticsearch_dsl.Q(t, text=terms) |
                elasticsearch_dsl.Q(t, author=terms) |
                elasticsearch_dsl.Q(t, title=terms) |
                elasticsearch_dsl.Q(t, category=terms) |
                elasticsearch_dsl.Q(t, location=terms)).to_queryset()
            time_range = eval('form.' + form['published'].value())  #### TODO !!! eval is evil.  
            search = len(queryset)
            if search and time_range:
                queryset = (queryset.filter(created_at__lt=time_range[0], created_at__gt=time_range[1])
                                    .order_by('-pinned')
                                    .select_related('author')
                                    .select_related('author__profile')
                                    .select_related('author__profile__avatar'))
                search = len(queryset)
            if not search:
                queryset = (artisan_models.Post.objects
                            .select_related('author')
                            .select_related('author__profile')
                            .select_related('author__profile__avatar')
                            .order_by('-pinned'))
        else:
            form.errors.clear()
            queryset = (artisan_models.Post.objects
                            .select_related('author')
                            .select_related('author__profile')
                            .select_related('author__profile__avatar')
                            .order_by('-pinned'))
         
        paginator = pagination.Paginator(queryset, self.paginate_by)
         
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'form': form,
            'page_obj': page_obj,
            'search': search,
            'is_a_search': is_a_search,
            'site_url': (request.scheme or 'https') + '://' + conf.settings.SITE_DOMAIN}
        return shortcuts.render(request, self.template_name, context)


class PostCreate(forum_views.PostCreate):
    model = artisan_models.Post
    form_class = artisan_forms.Post

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        post = form.save(commit=False)
        return super().form_valid(form, post)

    def get_success_url(self, post: artisan_models.Post, *args, **kwargs) -> str:
        return urls.reverse_lazy(
            'django_artisan:post_view', args=(
                post.id, post.slug,))

"""
    pings_google to recrawl site when user opts to list on about page
    or to display personal page
"""
def ping_google_func() -> None:
    try:
        sitemaps.ping_google()
        logger.info("Pinged Google!")
    except Exception as e:
        logger.error("unable to ping_google : {0}".format(e))

@decorators.method_decorator(cache.never_cache, name='dispatch')
class ArtisanForumProfile(forum_views.ForumProfile):
    """
        ForumProfile subclasses LoginRequiredMixin
    """
    model = artisan_models.ArtisanForumProfile
    post_model = artisan_models.Post 
    form_class = artisan_forms.ArtisanForumProfile
    user_form_class = forum_forms.ForumProfileUser
    success_url = urls.reverse_lazy('django_artisan:profile_update_view')
    template_name = 'django_artisan/profile/forum_profile_update_form.html'

    def populate_initial(self, user):
        super_dic = super().populate_initial(user)
        dic = { 
                    'bio': user.profile.bio,
                    'image_file': user.profile.image_file,
                    'shop_web_address': user.profile.shop_web_address,
                    'outlets': user.profile.outlets,
                    'listed_member': user.profile.listed_member,
                    'display_personal_page': user.profile.display_personal_page
                }
        dic.update(super_dic)
        return dic

    def post(self, request:http.HttpRequest) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: # type: ignore
            form = self.form_class(request.POST)
            user_form = self.user_form_class(request.POST)
            f_valid = False
            u_valid = False
            context = {}

            if form.is_valid():
                self.f_valid = True
                form.initial = self.populate_initial(request.user)
                if form.has_changed():
                    if ('display_personal_page' in form.changed_data or
                       'listed_member' in form.changed_data):
                        try:
                            if not conf.settings.DEBUG:
                                tasks.async_task(ping_google_func)
                        except:
                            tasks.async_task(ping_google_func)
                    profile = self.model.objects.get(profile_user=request.user)

                    #obj = form.save(commit=False)
                    #obj.profile_user = request.user
                    #obj.save()
                    breakpoint()
                    for change in form.changed_data:
                        if change == 'image_file':
                            img = Image.open(form['image_file'].value().path)
                            img = ImageOps.expand(img, border=10, fill='white')
                            img.save(form['image_file'].value().path)
                        setattr(profile,change,form[change].value())
                    profile.save(update_fields=form.changed_data)
            else:
                self.f_valid = False

            user_form.is_valid()
            try:
                user_form.errors.pop('username')
            except KeyError:
                pass
            if len(user_form.errors):
                self.u_valid = False
            else:
                self.u_valid = True
                user = auth.get_user_model().objects.get(username=user_form['username'].value())
                for change in user_form.changed_data:
                    setattr(user,change,user_form[change].value())
                user.save(update_fields=user_form.changed_data)
            breakpoint()
            if not self.f_valid or not self.u_valid:  
                return shortcuts.render(request, self.template_name, self.get_context_data())
            else:
                return super().post(request)

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        #context = {}
        site = site_models.Site.objects.get_current()
        context['form'].initial = {
                'bio': self.request.user.profile.bio,
                'image_file': self.request.user.profile.image_file,
                'shop_web_address': self.request.user.profile.shop_web_address,
                'outlets': self.request.user.profile.outlets,
                'listed_member': self.request.user.profile.listed_member,
                'display_personal_page': self.request.user.profile.display_personal_page
        }
        context['avatar'] = (artisan_models.ArtisanForumProfile.objects
                               .get(profile_user=self.request.user).avatar)
        queryset = (artisan_models.Post.objects
                               .select_related('author')
                               .select_related('author__profile')
                               .filter(author=self.request.user))
        paginator = pagination.Paginator(queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context ['site_url'] = (('https' if self.request.is_secure else 'http')
                                + '://'
                                + conf.settings.SITE_DOMAIN)
        return context


class AboutPage(generic.list.ListView):
    model = artisan_models.Event
    template_name = 'django_artisan/about.html'
    
    def get_context_data(self, **kwargs) -> dict:
        site = site_models.Site.objects.get_current()
        data = super().get_context_data(**kwargs)
        data['about_text'] = conf.settings.ABOUT_US_SPIEL
        data['site_url'] = (self.request.scheme or 'https') + '://' + site.domain
        qs = artisan_models.ArtisanForumProfile.objects.all().exclude(profile_user__is_superuser=True).exclude(listed_member=False) \
                                       .values_list('display_name', 'avatar__image_file')
        if qs.exists():
            data['people'] = {}
            for i, entry in enumerate(qs):
                data['people'][i] = {'display_name':entry[0], 'avatar':entry[1]}

        data['colours'] = ['text-white', 'text-purple', 'text-warning', 'text-lightgreen', 'text-danger', 'headline-text', 'sub-headline-text']
        return data

    def get_queryset(self) -> db_models.QuerySet:
            """Return all published posts."""
             # filter objects created today
            qs_bydate = self.model.objects.filter(time__gt=utils.timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
            qs_repeating = self.model.objects.filter(repeating=True)
            return qs_bydate | qs_repeating


class LandingPage(generic.base.TemplateView):
    model = artisan_models.UserProductImage
    template_name = 'django_artisan/landing_page.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['images'] = (artisan_models.UserProductImage.objects
                                       .select_related('user_profile')
                                       .filter(active=True))
        context['randomize_images'] = conf.settings.CAROUSEL_RANDOMIZE_IMAGES
        context['use_cache'] = conf.settings.CAROUSEL_USE_CACHE
        context['offset'] = conf.settings.CAROUSEL_OFFSET
        context['loading_image'] = 'django_bs_carousel/images/spinning-circles.svg'
        context['image_size_large'] = conf.settings.IMAGE_SIZE_LARGE
        context['image_size_small'] = conf.settings.IMAGE_SIZE_SMALL
        context['images_per_request'] = conf.settings.NUM_IMAGES_PER_REQUEST
        context['image_pause'] = conf.settings.CAROUSEL_IMG_PAUSE
        context['csrftoken'] = csrf.get_token(self.request)
        return context


class PersonalPage(generic.detail.DetailView):
    model = artisan_models.ArtisanForumProfile
    slug_url_kwarg = 'name_slug'
    slug_field = 'display_name'
    template_name = 'django_artisan/personal_page.html'

    def get_queryset(self) -> db_models.QuerySet:  #TODO: try/except clause
        return self.model.objects.filter(display_name=self.request.resolver_match.kwargs['name_slug'])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['images'] = (artisan_models.UserProductImage.objects
                                       .select_related('user_profile')
                                       .filter(user_profile=self.object)
                                       .filter(active=True))
        context['randomize_images'] = conf.settings.CAROUSEL_RANDOMIZE_IMAGES
        context['use_cache'] = conf.settings.CAROUSEL_USE_CACHE
        context['offset'] = conf.settings.CAROUSEL_OFFSET
        context['loading_image'] = 'django_bs_carousel/images/spinning-circles.svg'
        context['image_size_large'] = conf.settings.IMAGE_SIZE_LARGE
        context['image_size_small'] = conf.settings.IMAGE_SIZE_SMALL
        context['images_per_request'] = conf.settings.NUM_IMAGES_PER_REQUEST
        context['image_pause'] = conf.settings.CAROUSEL_IMG_PAUSE
        context['csrftoken'] = csrf.get_token(self.request)
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

    def get(self, request: http.HttpRequest, *args, **kwargs) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]:
        self.object = self.get_object() ## self.object is userprofile of requested person
        if self.object.display_personal_page or self.object.profile_user == self.request.user:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect(self.request.META.get('HTTP_REFERER'))


class UserProductImageUpload(mixins.LoginRequiredMixin, generic.edit.FormView):
    model = artisan_models.UserProductImage
    form_class = artisan_forms.UserProductImage
    template_name = 'django_artisan/profile/images/image_update.html'
    success_url = urls.reverse_lazy('django_artisan:image_update')
    
    @cache.never_cache
    def get(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = self.model.objects.filter(user_profile=self.request.user.profile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_artisan/profile/images/image_update.html', context)

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        obj = form.save(commit=False)
        obj.user_profile: artisan_forms.ArtisanForumProfile = self.request.user.profile
        obj.save()
        img = Image.open(obj.file.path)
        basewidth = 768
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img = ImageOps.expand(img, border=10, fill='white')
        img.save(obj.file.path)
        get_thumbnail(obj.file, conf.settings.IMAGE_SIZE_LARGE, 
                                    format="WEBP", crop='center', quality=70)
        get_thumbnail(obj.file, conf.settings.IMAGE_SIZE_SMALL, 
                                    format="WEBP", crop='center', quality=70)
        return redirect('django_artisan:image_update')

    def form_invalid(self, form: forms.ModelForm) -> http.HttpResponse:
        error_msg = str(form.errors)
        if len(form.errors['file']) > 1:
            message = 'The form is not valid. Fix the following errors...'
        else:
            message = 'The form is not valid. Fix the following error...'
        images = self.model.objects.filter(user_profile=self.request.user.profile)
        context = {'images': images, 'form': self.form_class(), 'message': message, 'error_msg': error_msg}
        return render(self.request, './django_artisan/profile/images/image_update.html', context)

    def get_form_kwargs(self, *args, **kwargs) -> dict:
        """
            to place user into form object for check maximum image count validator.
        """
        kwarg_dict = super().get_form_kwargs()
        kwarg_dict['user'] = self.request.user
        return kwarg_dict


class UserProductImageDelete(mixins.LoginRequiredMixin, generic.edit.UpdateView):
    http_method_names = ['post']
    model = artisan_models.UserProductImage
    slug_url_kwarg = 'del_id'
    slug_field = 'slug'
    success_url = urls.reverse_lazy('django_artisan:image_update')  
    template_name = 'django_artisan/profile/images/image_list.html'                  

    def post(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponseRedirect:
        artisan_models.UserProductImage.objects.get(del_id=self.kwargs['del_id']).delete()
        return redirect(self.success_url)

    def get_object(self, queryset=None, *args, **kwargs) -> typing.Union[artisan_models.UserProductImage, 
                                                                         http.HttpResponseRedirect,
                                                                         http.HttpResponsePermanentRedirect]:
        try:
            image = artisan_models.UserProductImage.objects.get(del_id=self.kwargs['del_id'])
        except artisan_models.UserProductImage.DoesNotExist as e:
            logger.error("Unable to get UserProductImage when deleting : {0}".format(e))
            image = None
        if image is None:
            return redirect(self.success_url)
        else:
            return image
