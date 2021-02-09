
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django_profile.views import ProfileUpdateView
from django.forms.models import model_to_dict 
from .models import ProfileImage, ForumProfile
from .forms import ProfileImageForm, ForumProfileDetailForm, \
                                     ForumProfileUserForm

### START PROFILE

class ForumProfileUpdateView(LoginRequiredMixin, ProfileUpdateView):
    model = ForumProfile 
    form_class = ForumProfileDetailForm
    user_form_class = ForumProfileUserForm
    success_url = reverse_lazy('forum_profile_update_view')
    template_name = 'django_forum_app/forum_profile_update_form.html'

    def form_valid(self, form):
        if form.has_changed():
            if form.is_valid():
                for change in form.changed_data:
                    setattr(self.request.user.profile.forumprofile, change, form[change].value())
                self.request.user.profile.forumprofile.save()
        return super().form_valid(form)
   

class ForumProfileUploadView(LoginRequiredMixin, FormView):
    model = ProfileImage
    form_class = ProfileImageForm
    template_name = 'django_forum_app/image_update.html'
    success_url = reverse_lazy('forum_profile_upload_view')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        message = 'Choose a file and add some accompanying text and a shop link if you have one'
        images = ProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_forum_app/image_update.html', context)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_profile = self.request.user.profile.forumprofile
        obj.save()
        message = 'Success!'
        images = ProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': form, 'message': message}
        return render(self.request, './django_forum_app/image_update.html', context)

    def form_invalid(self, form):
        message = 'The form is not valid. Fix the following error:'
        images = ProfileImage.objects.filter(user_profile=self.request.user.profile.forumprofile)
        context = {'images': images, 'form': self.form_class(), 'message': message}
        return render(self.request, './django_forum_app/image_update.html', context)

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
    model = ProfileImage
    slug_url_kwarg = 'unique_id'
    slug_field = 'slug'
    success_url = reverse_lazy('forum_profile_upload_view')  
    template_name = 'django_forum_app/image_list.html'                  

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

### END PROFILE