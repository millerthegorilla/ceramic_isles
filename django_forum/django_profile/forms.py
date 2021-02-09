from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, Div
from .fields import FloatingField
from .models import Profile
from django.forms.models import model_to_dict, fields_for_model

class ProfileUserForm(ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            self.add_error('username', 'Error, That username already exists!')
        return username
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.initial = kwargs['initial']
        except KeyError:
            pass
        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None
        self.helper = FormHelper()
        self.helper.css_class =''
        self.helper.layout = Layout(
                FloatingField('username'),
                FloatingField('email'),
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
        fields = ['username', 'email']
    


class ProfileDetailForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['user_slug', 'profile_user',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 


from django.forms.models import model_to_dict, fields_for_model


# class UserDetailsForm(ModelForm):
#     def __init__(self, instance=None, *args, **kwargs):
#         _fields = ('first_name', 'last_name', 'email',)
#         _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
#         super(UserDetailsForm, self).__init__(initial=initial, instance=instance, *args, **kwargs)
#         self.fields.update(fields_for_model(User, _fields))

#     class Meta:
#         model = UserDetails
#         exclude = ('user',)

#     def save(self, *args, **kwargs):
#         u = self.instance.user
#         u.first_name = self.cleaned_data['first_name']
#         u.last_name = self.cleaned_data['last_name']
#         u.email = self.cleaned_data['email']
#         u.save()
#         profile = super(UserDetailsForm, self).save(*args,**kwargs)
#         return profile
