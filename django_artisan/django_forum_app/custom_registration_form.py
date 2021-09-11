from fuzzywuzzy import fuzz
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, fields, PasswordInput
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Button, Div
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import StrictButton

from .models import ForumProfile
from typing import Any


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)
    email = EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_username(self) -> Any:
        username = self.cleaned_data['username']
        if fuzz.ratio(username, self['display_name'].value()) > 69:
            self.add_error(
                'username',
                'Error! your username is too similar to your display name')
            self.valid = False
        return username

    def clean_display_name(self) -> Any:
        displayname = self.cleaned_data['display_name']
        dname = slugify(displayname)
        try:
            ForumProfile.objects.get(display_name=dname)
        except ForumProfile.DoesNotExist:
            return displayname
        self.add_error(
            'display_name', 'Error! That display name already exists!')
        self.valid = False
        return displayname

    def clean_email(self) -> Any:
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['display_name'] = fields.CharField(
            label='Display name',)
        #         help_text='<span class="tinfo">Your display name will be shown \
        #                    in the forum and will be part of the link to your personal page.  \
        #                    It must be *different* to your username. It must be unique.  \
        #                    Perhaps use your first name and last name, or maybe your business name. \
        #                    It will be converted to an internet friendly name when you save it. \
        #                    You can change it later...</span>',
        #     )
        self.fields['username'] = fields.CharField(
            label='Username',
            help_text='<span class="tinfo">Your username is used purely \
                           for logging in, and must be different to your display name. \
                           It must be unique. \
                           No one will see your username. Letters, digits and @/./+/-/_ only.</span>',)
        self.fields['password2'] = fields.CharField(
            label='Password again!',
            widget=PasswordInput,)
        self.fields['rules'] = fields.BooleanField(
            label='<span class="tinfo">I have read and agree with the <a class="tinfo" target="blank" href="/forum/rules/">Rules</a></span>')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = Layout(
            FloatingField('display_name',
                          autocomplete="new-password", autofocus=''),
            FloatingField('username'),
            FloatingField('email', autocomplete="new-password"),
            FloatingField('password1'),
            FloatingField('password2', autocomplete="new-password"),
            Field('rules', css_class="mb-3"),
            Field('captcha'),
        )
