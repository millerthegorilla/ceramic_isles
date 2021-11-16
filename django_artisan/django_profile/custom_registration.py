from fuzzywuzzy import fuzz

from captcha import fields as captcha_fields, widgets as captcha_widgets
from crispy_forms import helper, layout, bootstrap
from crispy_bootstrap5 import bootstrap5

from django import forms, urls
from django.contrib.auth import forms as auth_forms, models as auth_models

from . import models as profile_models


class CustomUserCreation(auth_forms.UserCreationForm):
    captcha = captcha_fields.ReCaptchaField(label='', widget=captcha_widgets.ReCaptchaV2Checkbox)
    email = forms.EmailField()

    class Meta(auth_forms.UserCreationForm.Meta):
        fields = auth_forms.UserCreationForm.Meta.fields + ('email', 'captcha',)

    def clean_username(self) -> str:
        username = self.cleaned_data['username']
        if fuzz.ratio(username, self['display_name'].value()) > 69:
            self.add_error(
                'username',
                'Error! your username is too similar to your display name')
            self.valid = False
        return username

    def clean_display_name(self) -> str:
        displayname = self.cleaned_data['display_name']
        dname = defaultfilters.slugify(displayname)
        try:
            profile_models.Profile.objects.get(display_name=dname)
        except profile_models.Profile.DoesNotExist:
            return displayname
        self.add_error(
            'display_name', 'Error! That display name already exists!')
        self.valid = False
        return displayname

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        try:
            auth_models.User.objects.get(email=email)
        except auth_models.User.DoesNotExist:
            return email
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['display_name'] = forms.fields.CharField(
            label='Display name',
        )
        self.helper = helper.FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = urls.reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = layout.Layout(
            layout.HTML('<span class="tinfo">Your display name \
                        must be *different* to your username.  It must be unique.\
                        You can change it later...</span>'),
            bootstrap5.FloatingField('display_name', autocomplete="new-password"),
            layout.HTML('<span class="tinfo">Your username is used purely \
                        for logging in, and must be different to your display name. \
                        It must be unique. \
                         No one will see your username.</span>'),
            bootstrap5.FloatingField('username'),
            bootstrap5.FloatingField('email', autocomplete="new-password"),
            bootstrap5.FloatingField('password1'),
            bootstrap5.FloatingField('password2', autocomplete="new-password"),
            layout.Field('captcha'),
        )
