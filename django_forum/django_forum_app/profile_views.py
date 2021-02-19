import random
from PIL import Image, ImageOps
from django.db.models import Max
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

from django_profile.views import ProfileUpdateView
from django.forms.models import model_to_dict
from django.conf import settings 
from .models import ForumProfileImage, ForumProfile
from .forms import ForumProfileImageForm, ForumProfileDetailForm, \
                                     ForumProfileUserForm

### START PROFILE

class ForumProfileUpdateView(LoginRequiredMixin, ProfileUpdateView):
    model = ForumProfile 
    form_class = ForumProfileDetailForm
    user_form_class = ForumProfileUserForm
    success_url = reverse_lazy('django_forum_app:profile_update_view')
    template_name = 'django_forum_app/profile/forum_profile_update_form.html'

    def form_valid(self, form):
        if form.has_changed():
            if form.is_valid():
                for change in form.changed_data:
                    setattr(self.request.user.profile.forumprofile, change, form[change].value())
                self.request.user.profile.forumprofile.save()
        return super().form_valid(form)

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        context['back_image'] = self.get_random_image()
        return context

    def get_random_image(self):
        max_id = ForumProfileImage.objects.all().aggregate(max_id=Max("id"))['max_id']
        if max_id is not None and max_id != 0:
            while True:
                pk = random.randint(1, max_id)
                image = ForumProfileImage.objects.filter(id=pk).first()
                if image:
                    return image
        else:
            if ForumProfileImage.objects.filter(image_text="back_image").count() == 0:
                users = get_user_model().objects.filter(username='dummy_user')
                if users.count() > 0:
                    user = users.first()
                else:
                    user = get_user_model().objects.create(username='dummy_user')
                image = ForumProfileImage.objects.create(image_text='back_image', image_file='default_backgrounds/default_background_1.jpg', user_profile=user.profile.forumprofile)
            else:
                image = ForumProfileImage.objects.get(image_text="back_image")
            return image


class ForumProfileUploadView(LoginRequiredMixin, FormView):
    model = ForumProfileImage
    form_class = ForumProfileImageForm
    template_name = 'django_forum_app/profile/images/image_update.html'
    success_url = reverse_lazy('forum_profile_upload_view')
    
    @never_cache
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = ForumProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_forum_app/profile/images/image_update.html', context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile.forumprofile
        obj.save()
        url = str(settings.BASE_DIR) + obj.image_file.url
        img = Image.open(url)
        img = ImageOps.expand(img, border=10, fill='white')
        img.save(url)

        return redirect('django_forum_app:image_update')

    def form_invalid(self, form):
        error_msg = str(form.errors)
        if len(form.errors['image_file']) > 1:
            message = 'The form is not valid. Fix the following errors...'
        else:
            message = 'The form is not valid. Fix the following error...'
        images = ForumProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': self.form_class(), 'message': message, 'error_msg': error_msg}
        return render(self.request, './django_forum_app/profile/images/image_update.html', context)

    def get_form_kwargs(self, *args, **kwargs):
        """
            to place user into form object for check maximum image count validator.
        """
        kwarg_dict = super(ForumProfileUploadView, self).get_form_kwargs()
        kwarg_dict['user'] = self.request.user
        return kwarg_dict


# TODO: prompt on deletion as security against path hack
class ForumProfileImageDeleteView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    model = ForumProfileImage
    slug_url_kwarg = 'unique_id'
    slug_field = 'slug'
    success_url = reverse_lazy('django_forum_app:image_update')  
    template_name = 'django_forum_app/profile/images/image_list.html'                  

    def post(self, request, *args, **kwargs):
        ForumProfileImage.objects.get(image_id=self.kwargs['unique_id']).delete()
        return redirect(self.success_url)

    def get_object(self, queryset=None, *args, **kwargs):
        try:
            image = ForumProfileImage.objects.get(id=self.kwargs['unique_id'])
        except Exception as e:
            print(e)
            image = None
        if image is None:
            redirect(self.success_url)
        else:
            return image

### END PROFILE