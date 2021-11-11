import logging

from crispy_forms import helper, layout
from crispy_bootstrap5 import bootstrap5

from django import forms, db
from django.contrib.auth import models as auth_models

from . import models as profile_models
# TODO: need to setup clamav.conf properly


logger = logging.getLogger('django_artisan')

class ProfileUser(forms.ModelForm):
    # def clean_username(self, *args, **kwargs):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username):
    #         self.add_error('username', 'Error, That username already exists!')
    #     return username

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        try:
            self.initial = kwargs['initial']
        except KeyError:
            pass
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.css_class = ''
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('username'),
            bootstrap5.FloatingField('email'),
            bootstrap5.FloatingField('first_name'),
            bootstrap5.FloatingField('last_name'),
        )

    def clean_username(self, *args, **kwargs) -> str:
        username = self.cleaned_data['username']
        if username != self.initial['username']:
            try:
                auth_models.User.objects.get(username=username)
            except auth_models.User.DoesNotExist:
                return username
            except db.IntegrityError as e:
                error_message = e.__cause__
                logger.error(error_message)
            self.valid = False
            self.add_error('username', 'Error, That username already exists!')
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        if email != self.initial['email']:
            try:
                auth_models.User.objects.get(email=email)
            except auth_models.User.DoesNotExist:
                return email
            except db.IntegrityError as e:
                error_message = e.__cause__
                logger.error(error_message)
            self.valid = False
            self.add_error('email', 'Error! That email already exists!')
        return email

    class Meta:
        model = auth_models.User
        fields = ['username', 'email', 'first_name', 'last_name']


class Profile(forms.ModelForm):
    class Meta:
        model = profile_models.Profile
        fields = ['profile_user', 'display_name']
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.css_class = ''
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('display_name'),
        )
