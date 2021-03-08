from safe_imagefield.forms import SafeImageField    ## TODO: need to setup clamav.conf properly
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, HTML, Div
from crispy_forms.helper import FormHelper

from django.conf import settings
from django import forms

from django_forum_app.forms import ForumProfileDetailForm

from .models import ArtisanForumProfile, UserProductImage
from .fields import FloatingField, FileInput


MAX_NUMBER_OF_IMAGES = settings.MAX_USER_IMAGES


class ArtisanForumProfileDetailForm(ForumProfileDetailForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)

    class Meta(ForumProfileDetailForm.Meta):
        model = ArtisanForumProfile
        fields = ForumProfileDetailForm.Meta.fields + [
                                                  'image_file', \
                                                  'shop_web_address', \
                                                  'outlets',
                                                 ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_file'].required = False
        self.fields['image_file'].label = 'A single image for your personal page, click Update Profile to upload it...'
        self.helper.layout.fields = self.helper.layout.fields + [ 
            Field('image_file', css_class="text-white"),
            HTML('<span class="text-white">Your shop web address to be displayed on your personal page</span>'),
            FloatingField('shop_web_address'),
            HTML('<span class="text-white">A comma separated list of outlets that sell your stuff, for your personal page.</span>'),
            FloatingField('outlets'),
        ]
        self.helper.form_id = 'id-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'


class UserProductImageForm(forms.ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = UserProductImage
        fields = ['image_file', 'image_title', 'image_text', 'image_shop_link', 'image_shop_link_title']

    def __init__(self, instance=None, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['image_file'].validators.append(self.restrict_amount)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                FileInput('image_file', name="image_file"),
                FloatingField('image_title'),
                FloatingField('image_text'),
                FloatingField('image_shop_link'),
                FloatingField('image_shop_link_title'),),
        )
        self.helper.form_id = 'id-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto col-xs-3'


    def restrict_amount(self, value):
        if self.user is not None:
            if UserProductImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError('User already has {} images'.format(MAX_NUMBER_OF_IMAGES))


# handles deletion
class UserProductImagesForm(forms.ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = UserProductImage
        fields = ['image_file', 'image_text', 'image_shop_link']
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['image_file'].validators.append(self.restrict_amount)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                FileInput('image_file', css_class="col-auto"),
                FloatingField('image_text', css_class="col-auto"),
                FloatingField('image_shop_link', css_class="col-auto"),),        
        )
        self.helper.form_id = 'id-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-12'


    def restrict_amount(self, value):
        if self.user is not None:
            if UserProductImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError(_('User already has {0} images'.format(MAX_NUMBER_OF_IMAGES)),
                                      code='max_image_limit',
                                      params={'value':'3'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()