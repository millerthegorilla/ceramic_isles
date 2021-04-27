import random
from PIL import Image, ImageOps
from sorl.thumbnail import delete

from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.core.paginator import Paginator
from django.conf import settings

from django_forum_app.forms import ForumProfileUserForm
from django_forum_app.views import ForumProfileUpdateView, CustomRegisterView
from django_forum_app.models import ForumPost

from .models import Event, UserProductImage, ArtisanForumProfile
from .forms import ArtisanForumProfileDetailForm, UserProductImageForm


@method_decorator(never_cache, name='dispatch')
class ArtisanForumProfileUpdateView(ForumProfileUpdateView):
    """
        ForumProfileUpdateView subclasses LoginRequiredMixin
    """
    model = ArtisanForumProfile 
    form_class = ArtisanForumProfileDetailForm
    user_form_class = ForumProfileUserForm
    success_url = reverse_lazy('django_artisan:profile_update_view')
    template_name = 'django_artisan/profile/forum_profile_update_form.html'

    def form_valid(self, form, **kwargs):
        if self.request.POST['type'] == 'update-profile':
            if form.has_changed():
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

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        # context['form'].initial.update(
        #             {'bio':self.request.user.profile.forumprofile.artisanforumprofile.bio,
        #              'image_file':self.request.user.profile.forumprofile.artisanforumprofile.image_file,
        #              'shop_web_address':self.request.user.profile.forumprofile.artisanforumprofile.shop_web_address,
        #              'outlets':self.request.user.profile.forumprofile.artisanforumprofile.outlets,
        #              'listed_member':self.request.user.profile.forumprofile.artisanforumprofile.listed_member})
        context['avatar'] = ArtisanForumProfile.objects.get(profile_user=self.request.user).avatar
        queryset = ForumPost.objects.filter(author=self.request.user.profile.display_name)
        paginator = Paginator(queryset, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class AboutPageView(ListView):
    model = Event
    template_name = 'django_artisan/about.html'
    
    def get_context_data(self):
        data = super().get_context_data()
        data['about_text'] = settings.ABOUT_US_SPIEL
        qs = ArtisanForumProfile.objects.all().exclude(profile_user__is_superuser=True).exclude(listed_member=False) \
                                       .values_list('display_name', 'avatar__image_file')
        if qs.count:
            data['people'] = {}
            for i, entry in enumerate(qs):
                data['people'][i] = {'display_name':entry[0], 'avatar':entry[1]}

        data['colours'] = ['text-white', 'text-purple', 'text-warning', 'text-lightgreen', 'text-danger', 'headline-text', 'sub-headline-text']
        return data

    def get_queryset(self):
            """Return all published posts."""
             # filter objects created today
            qs_bydate = self.model.objects.filter(time__gt=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
            qs_repeating = self.model.objects.filter(repeating=True)
            return qs_bydate | qs_repeating


class LandingPageView(TemplateView):
    model = UserProductImage
    template_name = 'django_artisan/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = UserProductImage.objects.filter(active=True).order_by('?')
        context['image_size'] = "1024x768"
        context['username'] = self.request.user.username
        return context


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

class PersonalPageView(DetailView):
    model = ArtisanForumProfile
    slug_url_kwarg = 'name_slug'
    slug_field = 'display_name'
    template_name = 'django_artisan/personal_page.html'

    def get_queryset(self):  #TODO: try/except clause
        return self.model.objects.filter(display_name=self.request.resolver_match.kwargs['name_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = UserProductImage.objects.filter(
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.display_personal_page or self.request.user.is_authenticated:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            return redirect('django_artisan:landing_page')



class UserProductImageUploadView(LoginRequiredMixin, FormView):
    model = UserProductImage
    form_class = UserProductImageForm
    template_name = 'django_artisan/profile/images/image_update.html'
    success_url = reverse_lazy('django_artisan:image_update')
    
    @never_cache
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = self.model.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_artisan/profile/images/image_update.html', context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile.forumprofile.artisanforumprofile
        obj.save()
        img = Image.open(obj.image_file.path)
        img = ImageOps.expand(img, border=10, fill='white')
        img.save(obj.image_file.path)
        return redirect('django_artisan:image_update')

    def form_invalid(self, form):
        error_msg = str(form.errors)
        if len(form.errors['image_file']) > 1:
            message = 'The form is not valid. Fix the following errors...'
        else:
            message = 'The form is not valid. Fix the following error...'
        images = self.model.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': self.form_class(), 'message': message, 'error_msg': error_msg}
        return render(self.request, './django_artisan/profile/images/image_update.html', context)

    def get_form_kwargs(self, *args, **kwargs):
        """
            to place user into form object for check maximum image count validator.
        """
        kwarg_dict = super().get_form_kwargs()
        kwarg_dict['user'] = self.request.user
        return kwarg_dict



# TODO: prompt on deletion as security against path hack
class UserProductImageDeleteView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    model = UserProductImage
    slug_url_kwarg = 'unique_id'
    slug_field = 'slug'
    success_url = reverse_lazy('django_forum_app:image_update')  
    template_name = 'django_forum_app/profile/images/image_list.html'                  

    def post(self, request, *args, **kwargs):
        UserProductImage.objects.get(image_id=self.kwargs['unique_id']).delete()
        return redirect(self.success_url)

    def get_object(self, queryset=None, *args, **kwargs):
        try:
            image = UserProductImage.objects.get(id=self.kwargs['unique_id'])
        except Exception as e:
            print(e)
            image = None
        if image is None:
            redirect(self.success_url)
        else:
            return image


