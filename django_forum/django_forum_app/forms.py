from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, HTML, Div
from tinymce.widgets import TinyMCE

from django_profile.forms import ProfileUserForm, ProfileDetailForm
from django_posts_and_comments.forms import PostCreateForm, CommentForm
from .models import ForumProfile, ForumPost, ForumComment
from .fields import FloatingField, FileInput


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
        fields = ProfileDetailForm.Meta.fields + [
                                                  'address_line_1', \
                                                  'address_line_2', \
                                                  'parish', \
                                                  'postcode', \
                                                 ]
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
                HTML('<span class="tinfo">Your display name is used in the forum, and to make \
                        your personal page address.  Try your first name and last name, \
                        or use your business name.  It *must* be different to your username.  It will be \
                        converted to an internet friendly name when you save it.</span>'),
                FloatingField('display_name'),
                HTML('<span class="tinfo">Address details are only necessary if there is mail for users</span>'),
                HTML('<a class="btn btn-primary mb-3" data-bs-toggle="collapse" \
                     href="#collapseAddress" role="button" aria-expanded="false" \
                     aria-controls="collapseAddress">Address details</a><br>'),
                Div(
                FloatingField('address_line_1'),
                FloatingField('address_line_2'),
                FloatingField('parish'),
                FloatingField('postcode'),
                css_class="collapse ps-3", id="collapseAddress"),
        )
        self.helper.form_id = 'id-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'


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
                Field('text', css_class="mb-3 post-create-form-text"),
                HTML("<div class='font-italic mb-3 tinfo'>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</div>"),
                Div(Field('category'), css_class="tinfo"),
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
                        Field('text', css_class="comment-form-text"),
                        Div(HTML('<span>...characters left: 500</span>'), 
                            id="count", css_class="ms-auto tinfo"),
                               css_class="d-flex flex-column"),
                        css_class="d-flex flex-row align-items-end"),
                Submit('save', 'comment', css_class="col-auto mt-3"),
            css_class="tinfo")
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
