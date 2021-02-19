from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, HTML, Div
from tinymce.widgets import TinyMCE

from django_profile.forms import ProfileUserForm, ProfileDetailForm
from django_posts_and_comments.forms import PostCreateForm, CommentForm
from .models import ForumProfile, ForumProfileImage, ForumPost, ForumComment
from .fields import FloatingField, FileInput

from safe_filefield.forms import SafeImageField    ## TODO: need to setup clamav.conf properly

### START FORUMPROFILE


class ForumProfileUserForm(ProfileUserForm):
    # class Meta(ProfileUserForm.Meta):
    #     fields = ProfileUserForm.Meta.fields
    #     model = ProfileUserForm.Meta.model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False



class ForumProfileDetailForm(ProfileDetailForm):
    class Meta(ProfileDetailForm.Meta):
        model = ForumProfile
        fields = ProfileDetailForm.Meta.fields + ['first_name', \
                                                  'last_name', \
                                                  'bio', \
                                                  'shop_web_address', \
                                                  'outlets']
        exclude = ['user_slug', 'profile_user']

    def __init__(self, *args, **kwargs):
        # breakpoint()
        # _user_fields = ('username', 'email',)
        # _initial = model_to_dict(instance.user, _user_fields) if instance is not None else {}
        # super(UserDetailsForm, self).__init__(initial=initial, instance=instance, *args, **kwargs)
        # self.fields.update(fields_for_model(, _user_fields))
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
                FloatingField('first_name'),
                FloatingField('last_name'),
                FloatingField('bio'),
                FloatingField('shop_web_address'),
                FloatingField('outlets'),
        )
        self.helper.form_id = 'id-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'


MAX_NUMBER_OF_IMAGES = settings.MAX_USER_IMAGES


class ForumProfileImageForm(forms.ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = ForumProfileImage
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
            if ForumProfileImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError('User already has {} images'.format(MAX_NUMBER_OF_IMAGES))


# handle deletion
class ForumProfileImages(forms.ModelForm):
    image_file = SafeImageField(allowed_extensions=('jpg','png'), 
                               check_content_type=True, 
                               scan_viruses=True, 
                               media_integrity=True,
                               max_size_limit=2621440)
    class Meta:
        model = ForumProfileImage
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
            if ForumProfileImage.objects.filter(user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise ValidationError(_('User already has {0} images'.format(MAX_NUMBER_OF_IMAGES)),
                                      code='max_image_limit',
                                      params={'value':'3'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()


###  ENDPROFILE

###  START POST AND COMMENTS

class ForumPostCreateForm(PostCreateForm):
    class Meta(PostCreateForm.Meta):
        model = ForumPost
        fields = PostCreateForm.Meta.fields + ['category']
        widgets = { 'text': TinyMCE(attrs={'plugins':'wordcount', 'init_instance_callback': 'function (editor) { $(editor.getContainer()).find("button.tox-statusbar__wordcount").click();}',})}
        labels = { 'category':'Choose a category for your post...'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Create your post...',
                FloatingField('title'),
                Field('text', css_class="mb-3", style="min-height:60vh"),
                HTML("<div class='font-italic mb-3 text-white'>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</div>"),
                Div(Field('category'), css_class="text-white"),
                Submit('save', 'Publish Post', css_class="col-3 mt-3 mb-3"),
            )
        )
        self.helper.form_action = 'django_forum_app:post_create_view'


class ForumCommentForm(CommentForm):
    class Meta:
        model = ForumComment
        fields = CommentForm.Meta.fields + []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset(
                'Comment away...!',
                Row(
                    Column(
                        Field('text', style="max-height:15vh"),
                        Div(HTML('<span>...characters left: 500</span>'), 
                            id="count", css_class="ms-auto text-white"),
                               css_class="d-flex flex-column"),
                        css_class="d-flex flex-row align-items-end"),
                Submit('save', 'comment', css_class="col-auto mt-3"),
            css_class="text-white")
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_forum_app:post_view'


class ForumPostListSearch(forms.Form):
    PUBLISHED_ANY = ''
    PUBLISHED_TODAY = '1'
    PUBLISHED_WEEK = '7'

    PUBLISHED_CHOICES = (
        (PUBLISHED_ANY, 'Any'),
        (PUBLISHED_TODAY, 'Today'),
        (PUBLISHED_WEEK, 'This week'),
    )

    q = forms.CharField(label='Search Query')
    published = forms.ChoiceField(choices=PUBLISHED_CHOICES, required=False, initial=PUBLISHED_ANY)
