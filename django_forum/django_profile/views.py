from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Profile
from .forms import ProfileDetailForm, ProfileUserForm


class ProfileUpdateView(UpdateView):
    form_class = ProfileDetailForm
    user_form_class = ProfileUserForm
    model = Profile
    success_url = reverse_lazy('profile_update_view')
    template_name = 'profile_update_form.html'

    def get_object(self):
        return self.model.objects.get(profile_user_id=self.request.user.id) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['user_form'] = self.user_form_class(initial={'username':self.request.user.username,
                                                                  'email':self.request.user.email })     
        return context

    def form_valid(self, form, *args, **kwargs):
        user_form = self.user_form_class(self.request.POST)
        user_form.initial = {'username':self.request.user.username,
                             'email':self.request.user.email }
        user_form.errors.clear()  ### django validates username against database automatically, but not email
        if user_form.has_changed():
            if user_form.is_valid():
                for change in user_form.changed_data:
                    setattr(self.request.user, change, user_form[change].value())
                self.request.user.save()
        return render(self.request, self.template_name, {'form': form, 'user_form': user_form})
