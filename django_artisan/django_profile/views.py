from typing import Any, Union

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, FormView
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseRedirect

from django_users_app.views import RegisterView

from .custom_registration_form import CustomUserCreationForm
from .models import Profile
from .forms import ProfileDetailForm, ProfileUserForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileDetailForm
    user_form_class = ProfileUserForm
    model = Profile
    success_url = reverse_lazy('django_profile:profile_update_view')
    template_name = 'django_profile/profile_update_form.html'

    def get_object(self) -> Profile:
        return self.model.objects.get(profile_user_id=self.request.user.id)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # if self.request.method == 'GET':
        context['user_form'] = self.user_form_class(
            initial={
                'username': self.request.user.username, # type: ignore
                'email': self.request.user.email,
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name})
        return context

    def form_valid(self, form: ModelForm) -> Union[HttpResponse, HttpResponseRedirect]: 
        user_form = self.user_form_class(self.request.POST)
        user_form.initial = {'username': self.request.user.username, # type: ignore
                             'email': self.request.user.email,
                             'first_name': self.request.user.first_name,
                             'last_name': self.request.user.last_name}
        # django validates username against database automatically, but not email
        # so I clear the errors from the database as my form is validating the username
        # independently of the database validation.
        # the is_valid function then populates errors.
        user_form.errors.clear()
        if not user_form.is_valid():
            return render(
                self.request,
                self.template_name,
                context={
                    'form': form,
                    'user_form': user_form})
        for change in user_form.changed_data:
            setattr(self.request.user, change, user_form[change].value())
        self.request.user.save()
        if form.has_changed():
            obj = form.save(commit=False)
            obj.display_name = slugify(form['display_name'].value())
            obj.save()
        return redirect(self.success_url)
        # return render(self.request: HttpRequest self.template_name, {'form': form,
        # 'user_form': user_form})


# NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegisterView
# path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),
class CustomRegisterView(RegisterView):
    form_class = CustomUserCreationForm

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect:
        user = form.save()
        user.profile.display_name = slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        super().form_valid(form, user)
        return redirect('password_reset_done')
