import uuid # used as custom salt 

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.conf import settings

from django_email_verification import send_email

from .forms import CustomUserCreationForm


class DashboardView(LoginRequiredMixin, TemplateView):
    http_method_names = ['get']
    template_name = 'django_users_app/dashboard.html'

    def get(self, request, *args, **kwargs):
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['number'] = random.randrange(1, 100)
        return context

class RegisterView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'django_users_app/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("password_reset_done")
    model = User
    
    def form_valid(self, form, user=None):
        if user is None:
            user = form.save()
        super().form_valid(form)
        send_email(user, custom_salt=uuid.uuid4())
        return redirect('password_reset_done')

class RulesPageView(TemplateView):
    template_name = 'django_users_app/rules.html'
    extra_context = { 'app_name': settings.APP_NAME }