# TODO: need to setup clamav.conf properly
#from typing import Any, Dict

from safe_imagefield import forms as safe_image_forms
from crispy_forms import layout
from crispy_forms import helper
from crispy_bootstrap5 import bootstrap5

from django.core import exceptions
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from django_forum import models as forum_models
from django_forum import forms as forum_forms
from django_messages import forms as messages_forms

from . import models as artisan_models
from . import fields as artisan_fields


class ArtisanForumPost(forum_forms.ForumPost):
    class Meta(forum_forms.ForumPost.Meta):
        model = artisan_models.ArtisanForumPost
        fields = forum_forms.ForumPost.Meta.fields + ['category', 'location']
        widgets = forum_forms.ForumPost.Meta.widgets
        labels = {'category': 'Choose a category for your post...',
                  'location': 'Which island...?'}

    def __init__(self, user_name: str = None, post: artisan_models.ArtisanForumPost = None, *args, **kwargs) -> None:
        super().__init__(user_name=user_name, post=post, *args, **kwargs)
        checked_string = ''
        if post and user_name and post.subscribed_users.filter(
                username=user_name).count():
            checked_string = 'checked'
        checkbox_string = '<input type="checkbox" id="subscribe_cb" name="subscribe" value="Subscribe" ' + \
            checked_string + '> \
                              <label for="subscribe_cb" class="tinfo">Subscribe to this post...</label><br>'
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Create your post...',
                bootstrap5.FloatingField('title'),
                layout.Field('text', css_class="mb-3 post-create-form-text"),
                layout.HTML("<div class='font-italic mb-3 tinfo'>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</div>"),
                layout.Div(layout.Field('category', css_class="col-auto"), layout.Field('location',
                    css_class="col-auto"), css_class="col-8 col-sm-4 col-md-4 col-lg-3 tinfo"),
                layout.HTML(checkbox_string),
                layout.Submit('save', 'Publish Post', css_class="col-auto mt-3 mb-3"),
            )
        )
        self.helper.form_action = 'django_artisan:post_create_view'


# class ArtisanForumComment(forum_forms.ForumComment):
#     class Meta(forum_forms.ForumComment.Meta):
#         model = artisan_models.ArtisanForumComment
#         fields = forum_forms.ForumComment.Meta.fields


class ArtisanForumProfile(forum_forms.ForumProfile):
    image_file = safe_image_forms.SafeImageField(allowed_extensions=('jpg', 'png'),
                                                 check_content_type=True,
                                                 scan_viruses=True,
                                                 media_integrity=True,
                                                 max_size_limit=2621440)

    class Meta(forum_forms.ForumProfile.Meta):
        model = artisan_models.ArtisanForumProfile
        fields = forum_forms.ForumProfile.Meta.fields + [
            'image_file',
            'bio',
            'shop_web_address',
            'outlets',
            'listed_member',
            'display_personal_page',
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['image_file'].widget.is_required = False
        self.fields['image_file'].required = False
        self.fields['image_file'].help_text = '<span class="text-white">A single image for your personal page, click Update Profile to upload it...</span>'
        self.fields['bio'] = forms.fields.CharField(
            label="Biographical Information",
            help_text='<span class="text-white">Biographical detail is a maximum 500 character space to display \
                                     on your personal page.</span>',
            widget=forms.Textarea(),
            required=False)
        self.fields['shop_web_address'] = forms.fields.CharField(
            label='Your Online Shop Web Address',
            help_text='<span class="tinfo">Your shop web address to be displayed on your personal page</span>',
            required=False)
        self.fields['outlets'] = forms.fields.CharField(
            label='Outlets that sell your wares',
            help_text='<span class="tinfo">A comma separated list of outlets that sell your stuff, for your personal page.</span>',
            required=False)
        # add to the super class fields
        self.helper.layout.fields = self.helper.layout.fields + [
            artisan_fields.FileClearInput(
                'image_file', css_class="tinfo form-control form-control-lg"),
            bootstrap5.FloatingField('bio'),
            bootstrap5.FloatingField('shop_web_address'),
            bootstrap5.FloatingField('outlets'),
            layout.Div(layout.Field('listed_member'), css_class="tinfo"),
            layout.Div(layout.Field('display_personal_page'), css_class="tinfo"),
        ]
        self.helper.form_id = 'id-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto tinfo'


MAX_NUMBER_OF_IMAGES = settings.MAX_USER_IMAGES


class UserProductImage(forms.ModelForm):
    image_file = safe_image_forms.SafeImageField(allowed_extensions=('jpg', 'png'),
                                                 check_content_type=True,
                                                 scan_viruses=True,
                                                 media_integrity=True,
                                                 max_size_limit=2621440)

    class Meta:
        model= artisan_models.UserProductImage
        fields = ['image_file', 'image_title', 'image_text',
                  'image_shop_link', 'image_shop_link_title']

    def __init__(self, instance: 'UserProductImage' = None, user: User = None, *args, **kwargs) -> None:
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['image_file'].validators.append(self.restrict_amount)
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                            '',
                            artisan_fields.FileInput('image_file', name="image_file"),
                            bootstrap5.FloatingField('image_title'),
                            bootstrap5.FloatingField('image_text'),
                            bootstrap5.FloatingField('image_shop_link'),
                            bootstrap5.FloatingField('image_shop_link_title'),),
        )
        self.helper.form_id = 'id-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto col-xs-3'

    def restrict_amount(self, count: int) -> None:
        if artisan_models.UserProductImage.objects.count() and self.user is not None:
            if artisan_models.UserProductImage.objects.filter(
                    user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
                raise exceptions.ValidationError(
                    'User already has {} images'.format(MAX_NUMBER_OF_IMAGES))


class ArtisanForumPostListSearch(forum_forms.ForumPostListSearch):
    # category = forms.ChoiceField(
    #     choices=settings.CATEGORY.choices, required=False, initial=settings.CATEGORY.GENERAL)
    # location = forms.ChoiceField(
    #     choices=settings.LOCATION.choices, required=False, initial=settings.LOCATION.ANY_ISLE)

    class Meta(forum_forms.ForumPostListSearch.Meta):
        fields = forum_forms.ForumPostListSearch.Meta.fields + ['search']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '',
                layout.Field('q', wrapper_class="col-12 col-sm-8 col-md-6 col-lg-4"),
                layout.Field('published', wrapper_class="mb-3 col-lg-auto col-12", css_class=""),
                layout.Submit('Search', 'search', css_class="col-auto mt-3"),
                css_class="text-white row justify-content-center align-items-center"
            ),
        )
        self.helper.form_id = 'id-search-form'
        self.helper.form_method = 'get'
        self.helper.form_class = 'search-form col-12 col-sm-12 col-md-10 col-lg-6 text-white'

# handles deletion  ## TODO is this even used?
# class UserProductImageDelete(forms.ModelForm):
#     image_file = safe_image_forms.SafeImageField(allowed_extensions=('jpg', 'png'),
#                                                  check_content_type=True,
#                                                  scan_viruses=True,
#                                                  media_integrity=True,
#                                                  max_size_limit=2621440)

#     class Meta:
#         model = UserProductImage
#         fields = ['image_file', 'image_text', 'image_shop_link']

#     def __init__(self, user: User = None, *args, **kwargs) -> None:
#         self.user = user
#         super().__init__(*args, **kwargs)
#         self.fields['image_file'].validators.append(self.restrict_amount)

#         self.helper = helper.FormHelper()
#         self.helper.layout = layout.Layout(
#             layout.Fieldset(
#                     '',
#                     FileInput('image_file', css_class="col-auto"),
#                     boostrap5.FloatingField('image_text', css_class="col-auto"),
#                     boostrap5.FloatingField('image_shop_link', css_class="col-auto"),),
#         )
#         self.helper.form_id = 'id-upload-form'
#         self.helper.form_method = 'post'
#         self.helper.form_class = 'col-12'

#     def restrict_amount(self) -> None:
#         if self.user is not None:
#             if UserProductImage.objects.filter(
#                     user_profile=self.user.profile.forumprofile).count() >= MAX_NUMBER_OF_IMAGES:
#                 raise exceptions.ValidationError(_('User already has {0} images'.format(
#                     MAX_NUMBER_OF_IMAGES)), code='max_image_limit', params={'value': '3'})

#     def clean(self) -> Dict[str, Any]:
#         cleaned_data = super().clean()
#         return cleaned_data
