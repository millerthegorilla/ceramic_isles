from fuzzywuzzy import fuzz
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, fields
from django.urls import reverse_lazy

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset, HTML, Button, Div
from crispy_forms.bootstrap import StrictButton
from .fields import FloatingField


class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox)
    email = EmailField()
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_username(self):
        username = self.cleaned_data['username']
        if fuzz.ratio(username, self['display_name'].value()) > 69:
            self.add_error('username', 'Error! your username is too similar to your display name')
            self.valid = False
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email          
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'] = fields.CharField(
                label='Display name',
                help_text='display name',
            )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = Layout(
                HTML('<span class="tinfo">Your display name \
                        must be *different* to your username. \
                        You can change it later...</span>'),
                FloatingField('display_name', autocomplete="new-password"),
                HTML('<span class="tinfo">Your username is used purely \
                        for logging in, and must be different to your display name. \
                         No one will see your username.</span>'),
                FloatingField('username', autocomplete="new-password"),
                FloatingField('email', autocomplete="new-password"),
                FloatingField('password1', autocomplete="new-password"),
                FloatingField('password2', autocomplete="new-password"),
                Field('captcha'),
            )