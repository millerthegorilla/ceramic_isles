from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, Div
from .fields import FloatingField
from .models import Profile, ProfileImage
from safe_filefield.forms import SafeImageField    ## TODO: need to setup clamav.conf properly


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 


MAX_NUMBER_OF_IMAGES = settings.MAX_USER_IMAGES


class ProfileImageForm(ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = ProfileImage
        fields = ['image_file']

    def __init__(self, instance=None, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['image_file'].validators.append(self.restrict_amount)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                FileInput('image_file', name="image_file"),),
        )
        self.helper.form_id = 'id-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto col-xs-3'


    def restrict_amount(self, value):
        if self.user is not None:
            if ProfileImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError('User already has {} images'.format(MAX_NUMBER_OF_IMAGES))


# handle deletion
class ProfileImages(ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = ProfileImage
        fields = ['image_file']
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['image_file'].validators.append(self.restrict_amount)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                FileInput('image_file', css_class="col-auto"),),        
        )
        self.helper.form_id = 'id-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-12'


    def restrict_amount(self, value):
        if self.user is not None:
            if ProfileImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError(_('User already has {0} images'.format(MAX_NUMBER_OF_IMAGES)),
                                      code='max_image_limit',
                                      params={'value':'3'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()


