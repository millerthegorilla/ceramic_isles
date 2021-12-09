import captcha
import crispy_forms
from crispy_bootstrap5 import bootstrap5
from fuzzywuzzy import fuzz
from itertools import chain

from django.contrib import auth
from django import forms
from django.urls import reverse_lazy
from django.template import defaultfilters

from . import models as forum_models


class CustomUserCreation(auth.forms.UserCreationForm):
    captcha = captcha.fields.ReCaptchaField(label='', widget=captcha.widgets.ReCaptchaV2Checkbox)
    email = forms.EmailField()
    model = forum_models.ForumProfile
    
    class Meta(auth.forms.UserCreationForm.Meta):
        fields = (*auth.forms.UserCreationForm.Meta.fields, 'email', 'captcha',)

    # def save(self, commit:bool = True, profile_model = forum_models.ForumProfile) -> "CustomUserCreation":
    #     instance = super().save(commit=False)
    #     instance.profile_model = profile_model
    #     if commit:
    #         instance.save()
    #     return instance

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
            self.model.objects.get(display_name=dname)
        except self.model.DoesNotExist:
            return displayname
        self.add_error(
            'display_name', 'Error! That display name already exists!')
        self.valid = False
        return displayname

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        try:
            auth.models.User.objects.get(email=email)
        except auth.models.User.DoesNotExist:
            return email
        self.add_error('email', 'Error! That email already exists!')
        self.valid = False
        return email

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['display_name'] = forms.fields.CharField(
            label='Display name',)
        #         help_text='<span class="tinfo">Your display name will be shown \
        #                    in the forum and will be part of the link to your personal page.  \
        #                    It must be *different* to your username. It must be unique.  \
        #                    Perhaps use your first name and last name, or maybe your business name. \
        #                    It will be converted to an internet friendly name when you save it. \
        #                    You can change it later...</span>',
        #     )
        self.fields['username'] = forms.fields.CharField(
            label='Username',
            help_text='<span class="tinfo">Your username is used purely \
                           for logging in, and must be different to your display name. \
                           It must be unique. \
                           No one will see your username. Letters, digits and @/./+/-/_ only.</span>',)
        self.fields['password2'] = forms.fields.CharField(
            label='Password again!',
            widget=forms.PasswordInput,)
        self.fields['rules'] = forms.fields.BooleanField(
            label='<span class="tinfo">I have read and agree with the <a class="tinfo" target="blank" href="/forum/rules/">Rules</a></span>')
        self.helper = crispy_forms.helper.FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('register')
        self.helper.form_tag = False
        self.helper.form_class = ""
        self.helper.layout = crispy_forms.layout.Layout(
            bootstrap5.FloatingField('display_name',
                          autocomplete="new-password", autofocus=''),
            bootstrap5.FloatingField('username'),
            bootstrap5.FloatingField('email', autocomplete="new-password"),
            bootstrap5.FloatingField('password1'),
            bootstrap5.FloatingField('password2', autocomplete="new-password"),
            crispy_forms.layout.Field('rules', css_class="mb-3"),
            crispy_forms.layout.Field('captcha'),
        )
