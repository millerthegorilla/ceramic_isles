from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, Div
from .fields import FloatingField
from .models import Profile
from safe_imagefield.forms import SafeImageField    ## TODO: need to setup clamav.conf properly


class ProfileUserForm(ModelForm):
    # def clean_username(self, *args, **kwargs):
    #     breakpoint()
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username):
    #         self.add_error('username', 'Error, That username already exists!')
    #     return username
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.initial = kwargs['initial']
        except KeyError:
            pass
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.css_class =''
        self.helper.layout = Layout(
                FloatingField('username'),
                FloatingField('email'),
                FloatingField('first_name'),
                FloatingField('last_name'),
        )

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        if username != self.initial['username']:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            except IntegrityError as e:
                error_message = e.__cause__
                messages.error(None, error_message)
            self.valid = False
            self.add_error('username', 'Error, That username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.initial['email']:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            except IntegrityError as e:
                error_message = e.__cause__
                messages.error(None, error_message)
            self.valid = False 
            self.add_error('email', 'Error! That email already exists!')
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    


class ProfileDetailForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_user', 'display_name']
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.css_class =''
        self.helper.form_tag = False
        self.helper.layout = Layout(
                FloatingField('display_name'),
        )