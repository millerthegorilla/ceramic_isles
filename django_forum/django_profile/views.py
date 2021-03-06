from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, FormView
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Profile, ProfileImage
from .forms import ProfileDetailForm, ProfileUserForm, ProfileImageForm


class ProfileUpdateView(UpdateView):
    form_class = ProfileDetailForm
    user_form_class = ProfileUserForm
    model = Profile
    success_url = reverse_lazy('django_profile:profile_update')
    template_name = 'django_profile/profile_update_form.html'

    def get_object(self):
        return self.model.objects.get(profile_user_id=self.request.user.id) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['user_form'] = self.user_form_class(initial={'username':self.request.user.username,
                                                                  'email':self.request.user.email,
                                                                  'first_name':self.request.user.first_name,
                                                                  'last_name':self.request.user.last_name })     
        return context

    def form_valid(self, form, *args, **kwargs):
        user_form = self.user_form_class(self.request.POST)
        user_form.initial = {'username':self.request.user.username,
                             'email':self.request.user.email,
                             'first_name':self.request.user.first_name,
                             'last_name':self.request.user.last_name }
        user_form.errors.clear()  ### django validates username against database automatically, but not email
        if user_form.has_changed():
            if user_form.is_valid():
                for change in user_form.changed_data:
                    setattr(self.request.user, change, user_form[change].value())
                self.request.user.save()
        return render(self.request, self.template_name, {'form': form, 'user_form': user_form})


class ProfileUploadView(FormView):
    model = ProfileImage
    form_class = ProfileImageForm
    template_name = 'django_profile/images/image_update.html'
    success_url = reverse_lazy('django_profile:profile_upload_view')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = ProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_forum_app/profile/images/image_update.html', context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile.forumprofile
        obj.save()
        return redirect('image_update')

    def form_invalid(self, form):
        error_msg = str(form.errors)
        if len(form.errors['image_file']) > 1:
            message = 'The form is not valid. Fix the following errors...'
        else:
            message = 'The form is not valid. Fix the following error...'
        images = ProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
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
class ProfileImageDeleteView(UpdateView):
    http_method_names = ['post']
    model = ProfileImage
    slug_url_kwarg = 'unique_id'
    slug_field = 'slug'
    success_url = reverse_lazy('django_profile:profile_upload_view')  
    template_name = 'django_profile/images/image_list.html'                  

    def post(self, request, *args, **kwargs):
        ProfileImage.objects.get(id=self.kwargs['unique_id']).delete()
        return redirect(self.success_url)

    def get_object(self, queryset=None, *args, **kwargs):
        try:
            image = ProfileImage.objects.get(id=self.kwargs['unique_id'])
        except Exception as e:
            print(e)
            image = None
        if image is None:
            redirect(self.success_url)
        else:
            return image
