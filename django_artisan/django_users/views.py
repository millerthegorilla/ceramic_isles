import uuid  # used as custom salt

from django import shortcuts, forms
from django.contrib import auth
from django.views import generic
from django import urls, http, forms

from django_email_verification import send_email

from . import forms as users_forms


class Register(generic.edit.CreateView):
    http_method_names = ['get', 'post']
    template_name = 'django_users/register.html'
    form_class = users_forms.CustomUserCreation
    success_url = urls.reverse_lazy("password_reset_done")
    model = auth.get_user_model()

    def form_valid(self, form: forms.ModelForm, user=None) -> http.HttpResponseRedirect:
        super().form_valid(form)
        if user is None:
            user = form.save()
        user.is_active = False
        user.save()
        send_email(user)
        return shortcuts.redirect('password_reset_done')


class ResendConfirmation(generic.FormView):
    http_method_names = ['get', 'post']
    template_name = 'django_users/resend_form.html'
    extra_context = {'instructions': 'Resend confirmation token'}
    form_class = users_forms.UserResendConfirmation
    success_url = 'django_users/registration_confirmation_sent.html'

    def form_valid(self, form, **kwargs) -> http.HttpResponse:
        super().form_valid(form)
        try:
            user = auth.get_user_model().objects.get(
                username=form['username'].value())
            if user.is_active is False:
                send_email(user)
                return shortcuts.render(self.request, self.success_url, {form: form})
            else:
                return shortcuts.render(self.request, self.template_name, {form: form})
        except auth.get_user_model().DoesNotExist:
            form.errors = [
                {'username': 'Hey you haven\'t registered yet.  Register first!'}]
            return shortcuts.render(self.request, self.template_name, {form: form})
