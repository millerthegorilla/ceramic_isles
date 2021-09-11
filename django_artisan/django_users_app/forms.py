from fuzzywuzzy import fuzz
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, fields, Form, CharField
from django.urls import reverse_lazy

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Button, Div
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField
from typing import Any


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)
    email = EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_email(self) -> Any:
        email = self.cleaned_data['email']
        try:
            user = get_user_model().objects.get(email=email)
        except User.DoesNotExist:
            return email
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('email', autocomplete="new-password"),
            FloatingField('password1'),
            FloatingField('password2', autocomplete="new-password"),
            Field('captcha'),
        )


class UserPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)

    def clean_email(self) -> Any:
        email = self.cleaned_data['email']
        try:
            user = get_user_model().objects.get(email=email)
            if user.is_active is False:
                self.valid = False
                self.add_error(
                    'email', 'Hey!, you haven\'t finished registering yet, \
                                         perhaps you want to resend a confiration token?')
                return email
        except User.DoesNotExist:
            self.valid = False
            self.add_error(
                'email', 'Hey!, you haven\'t registered, perhaps you want to try \
                                     registering first?')
            return email
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['email'].label = "Email Here!"
        self.helper.layout = Layout(
            FloatingField('email', css_class="mb3"),
            Field('captcha'),
            HTML('<div class="row justify-content-end"> \
                    <div class="col-auto"> \
                        <button class="btn btn-primary mt-3" type="submit">Send</button> \
                    </div> \
                  </div>')
        )


class UserResendConfirmationForm(Form):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)
    username = CharField(label='Your username here...')

    def clean_username(self, *args, **kwargs) -> Any:
        username = self.cleaned_data['username']
        try:
            user = get_user_model().objects.get(username=username)
            if user.is_active:
                self.valid = False
                self.add_error(
                    'username', 'Hey, you are already a registered member, perhaps you want to \
                                            Reset your password?')
                return username
        except User.DoesNotExist:
            self.valid = False
            self.add_error(
                'username',
                'Hey!  That username does not exist!  Try registering first.')
        return username

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ""
        self.helper.layout = Layout(
            FloatingField('username', wrapper_class="col-auto",
                          css_class="mb-3"),
            Field('captcha'),
            HTML('<div class="row justify-content-end"> \
                    <div class="col-auto"> \
                        <button class="btn btn-primary mt-3" type="submit">Send</button> \
                    </div> \
                  </div>')
        )
