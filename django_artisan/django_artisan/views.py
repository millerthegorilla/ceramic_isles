import random
import logging
from PIL import Image, ImageOps
from sorl.thumbnail import delete
from django_q.tasks import async_task
import typing

from django import http, forms
from django.core import paginator as pagination
from django.conf import settings
from django.contrib.auth import mixins
from django.contrib.sitemaps import ping_google
from django.contrib.sites import models as site_models
from django.db import models as db_models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import generic
from django.views.decorators.cache import never_cache

from django_forum import forms as forum_forms
from django_forum import views as forum_views
from django_forum import models as forum_models

from . import models as artisan_models
from . import forms as artisan_forms 

logger = logging.getLogger('django_artisan')

def ping_google_func() -> None:
    try:
        ping_google()
        logger.info("Pinged Google!")
    except Exception as e:
        logger.error("unable to ping_google : {0}".format(e))

@method_decorator(never_cache, name='dispatch')
class ArtisanForumProfile(forum_views.ForumProfile):
    """
        ForumProfile subclasses LoginRequiredMixin
    """
    model = artisan_models.ArtisanForumProfile 
    form_class = artisan_forms.ArtisanForumProfile
    user_form_class = forum_forms.ForumProfileUser
    success_url = reverse_lazy('django_artisan:profile_update_view')
    template_name = 'django_artisan/profile/forum_profile_update_form.html'

    ## TODO type form to correct type of Form - probably artisan_forms.ArtisanForumProfile
    ##  and do the same in superclasses
    def form_valid(self, form: forms.ModelForm, **kwargs) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: # type: ignore
    # - mypy grumbles about missing return statement coz it can't handle inheritance
        if self.request.POST['type'] == 'update-profile':
            if form.has_changed():
                if 'display_personal_page' in form.changed_data or \
                   'listed_member' in form.changed_data:
                   async_task(ping_google_func)
                obj = form.save()
                if obj.image_file:
                    img = Image.open(obj.image_file.path)
                    img = ImageOps.expand(img, border=10, fill='white')
                    img.save(obj.image_file.path)
            return super().form_valid(form)
            #return redirect(self.success_url)
        elif self.request.POST['type'] == 'update-avatar':
            super().form_valid(form)
            return redirect(self.success_url)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        site = site_models.Site.objects.get_current()
        # context['form'].initial.update(
        #             {'bio':self.request.user.profile.forumprofile.artisanforumprofile.bio,
        #              'image_file':self.request.user.profile.forumprofile.artisanforumprofile.image_file,
        #              'shop_web_address':self.request.user.profile.forumprofile.artisanforumprofile.shop_web_address,
        #              'outlets':self.request.user.profile.forumprofile.artisanforumprofile.outlets,
        #              'listed_member':self.request.user.profile.forumprofile.artisanforumprofile.listed_member})
        context['avatar'] = artisan_models.ArtisanForumProfile.objects.get(profile_user=self.request.user).avatar
        queryset = forum_models.ForumPost.objects.filter(author=self.request.user.profile.display_name)
        paginator = pagination.Paginator(queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context ['site_url'] = (self.request.scheme or 'https') + '://' + site.domain
        return context


class AboutPage(generic.list.ListView):
    model = artisan_models.Event
    template_name = 'django_artisan/about.html'
    
    def get_context_data(self, **kwargs) -> dict:
        site = site_models.Site.objects.get_current()
        data = super().get_context_data(**kwargs)
        data['about_text'] = settings.ABOUT_US_SPIEL
        data['site_url'] = (self.request.scheme or 'https') + '://' + site.domain
        qs = artisan_models.ArtisanForumProfile.objects.all().exclude(profile_user__is_superuser=True).exclude(listed_member=False) \
                                       .values_list('display_name', 'avatar__image_file')
        if qs.count:
            data['people'] = {}
            for i, entry in enumerate(qs):
                data['people'][i] = {'display_name':entry[0], 'avatar':entry[1]}

        data['colours'] = ['text-white', 'text-purple', 'text-warning', 'text-lightgreen', 'text-danger', 'headline-text', 'sub-headline-text']
        return data

    def get_queryset(self) -> db_models.QuerySet:
            """Return all published posts."""
             # filter objects created today
            qs_bydate = self.model.objects.filter(time__gt=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
            qs_repeating = self.model.objects.filter(repeating=True)
            return qs_bydate | qs_repeating


class LandingPage(generic.base.TemplateView):
    model = artisan_models.UserProductImage
    template_name = 'django_artisan/landing_page.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['images'] = artisan_models.UserProductImage.objects.filter(active=True).order_by('?')
        context['image_size'] = "1024x768"
        context['username'] = self.request.user.username # type: ignore
        return context

# class PeopleDirectoryView(TemplateView):
#     template_name = 'django_forum/people.html'

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

class PersonalPage(generic.detail.DetailView):
    model = artisan_models.ArtisanForumProfile
    slug_url_kwarg = 'name_slug'
    slug_field = 'display_name'
    template_name = 'django_artisan/personal_page.html'

    def get_queryset(self) -> db_models.QuerySet:  #TODO: try/except clause
        return self.model.objects.filter(display_name=self.request.resolver_match.kwargs['name_slug'])

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['images'] = artisan_models.UserProductImage.objects.filter(
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

    def get(self, request: http.HttpRequest, *args, **kwargs) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]:
        self.object = self.get_object()
        if self.object.display_personal_page or self.request.user.is_authenticated:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect('django_artisan:landing_page')



class UserProductImageUpload(mixins.LoginRequiredMixin, generic.edit.FormView):
    model = artisan_models.UserProductImage
    form_class = artisan_forms.UserProductImage
    template_name = 'django_artisan/profile/images/image_update.html'
    success_url = reverse_lazy('django_artisan:image_update')
    
    @never_cache
    def get(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = self.model.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_artisan/profile/images/image_update.html', context)

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile.forumprofile.artisanforumprofile
        obj.save()
        img = Image.open(obj.image_file.path)
        img = ImageOps.expand(img, border=10, fill='white')
        img.save(obj.image_file.path)
        return redirect('django_artisan:image_update')

    def form_invalid(self, form: forms.ModelForm) -> http.HttpResponse:
        error_msg = str(form.errors)
        if len(form.errors['image_file']) > 1:
            message = 'The form is not valid. Fix the following errors...'
        else:
            message = 'The form is not valid. Fix the following error...'
        images = self.model.objects.filter(user_profile=self.request.user.profile.forumprofile)
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
    slug_url_kwarg = 'unique_id'
    slug_field = 'slug'
    success_url = reverse_lazy('django_artisan:image_update')  
    template_name = 'django_artisan/profile/images/image_list.html'                  

    def post(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponseRedirect:
        artisan_models.UserProductImage.objects.get(image_id=self.kwargs['unique_id']).delete()
        return redirect(self.success_url)

    def get_object(self, queryset=None, *args, **kwargs) -> typing.Union[artisan_models.UserProductImage, 
                                                                         http.HttpResponseRedirect,
                                                                         http.HttpResponsePermanentRedirect]:
        try:
            image = artisan_models.UserProductImage.objects.get(id=self.kwargs['unique_id'])
        except artisan_models.UserProductImage.DoesNotExist as e:
            logger.error("Unable to get UserProductImage when deleting : {0}".format(e))
            image = None
        if image is None:
            return redirect(self.success_url)
        else:
            return image


