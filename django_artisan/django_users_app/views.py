import uuid  # used as custom salt

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.conf import settings

from django_email_verification import send_email

from .forms import CustomUserCreationForm, UserResendConfirmationForm
from typing import Any


class RegisterView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'django_users_app/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("password_reset_done")
    model = get_user_model()

    def form_valid(self, form, user=None) -> Any:
        super().form_valid(form)
        if user is None:
            user = form.save()
        user.is_active = False
        user.save()
        send_email(user)
        return redirect('password_reset_done')


class ResendConfirmationView(FormView):
    http_method_names = ['get', 'post']
    template_name = 'django_users_app/resend_form.html'
    extra_context = {'instructions': 'Resend confirmation token'}
    form_class = UserResendConfirmationForm
    success_url = 'django_users_app/registration_confirmation_sent.html'

    def form_valid(self, form, **kwargs) -> Any:
        super().form_valid(form)
        try:
            user = get_user_model().objects.get(
                username=form['username'].value())
            if user.is_active is False:
                send_email(user)
                return render(self.request, self.success_url, {form: form})
            else:
                return render(self.template_name, self.request, {form: form})
        except get_user_model().DoesNotExist:
            form.errors = [
                {'username': 'Hey you haven\'t registered yet.  Register first!'}]
            return render(self.request, self.template_name, {form: form})
