import typing

from django import shortcuts, forms, urls, http
from django.views import generic
from django.contrib.auth import mixins
from django.template import defaultfilters

import django_users.views as users_views

from . import custom_registration
from . import models as profile_models
from . import forms as profile_forms


class ProfileUpdate(mixins.LoginRequiredMixin, generic.edit.UpdateView):
    form_class = profile_forms.Profile
    user_form_class = profile_forms.ProfileUser
    model = profile_models.Profile
    success_url = urls.reverse_lazy('django_profile:profile_update_view')
    template_name = 'django_profile/profile_update_form.html'

    def get_object(self) -> profile_models.Profile:
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

    def form_valid(self, form: forms.ModelForm) -> typing.Union[http.HttpResponse, http.HttpResponseRedirect]: 
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
            return shortcuts.render(
                self.request,
                self.template_name,
                context={
                    'form': form,
                    'user_form': user_form})
        for change in user_form.changed_data:
            setattr(self.request.user, change, user_form[change].value())
        self.request.user.save()
        return shortcuts.redirect(self.success_url)
        # return render(self.request: HttpRequest self.template_name, {'form': form,
        # 'user_form': user_form})


# NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),
class CustomRegister(users_views.Register):
    form_class = custom_registration.CustomUserCreation

    def form_valid(self, form: forms.ModelForm) -> http.HttpResponseRedirect:
        user = form.save()
        user.profile.display_name = defaultfilters.slugify(form['display_name'].value())
        user.profile.save(update_fields=['display_name'])
        super().form_valid(form, user)
        return shortcuts.redirect('password_reset_done')
