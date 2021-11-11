import crispy_forms
from crispy_bootstrap5 import bootstrap5 
from tinymce.widgets import TinyMCE

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from django_profile import forms as profile_forms
from django_posts_and_comments import forms as posts_and_comments_forms

from . import models as forum_models


# START FORUMPROFILE
# class AvatarForm(forms.Form):
#     def __init__(*args, **kwargs):


class ForumProfileUserForm(profile_forms.ProfileUserForm):
    class Meta(profile_forms.ProfileUserForm.Meta):
        fields = profile_forms.ProfileUserForm.Meta.fields
        model = profile_forms.ProfileUserForm.Meta.model

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if len(args):   # TODO review this...
            initl = args[0].get('display_name')
        else:
            initl = forum_models.ForumProfile.objects.get(
                profile_user__username=kwargs['initial']['username']).display_name
        self.fields['display_name'] = forms.CharField(
            help_text='<span class="tinfo">Your display name is used in the forum, and to make \
                        your personal page address.  Try your first name and last name, \
                        or use your business name.  It *must* be different to your username.  It will be \
                        converted to an internet friendly name when you save it.</span>', initial=initl)
        self.helper.form_tag = False
        self.helper.layout = crispy_form.layout.Layout(
            bootstrap5.FloatingField('display_name'),
            self.helper.layout)


class ForumProfileDetailForm(profile_forms.ProfileDetailForm):
    class Meta(profile_forms.ProfileDetailForm.Meta):
        model = forum_models.ForumProfile
        fields = profile_forms.ProfileDetailForm.Meta.fields + [
            'address_line_1',
            'address_line_2',
            'parish',
            'postcode',
        ]
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = crispy_forms.helper.FormHelper()
        self.helper.form_tag = False
        self.helper.layout = crispy_forms.layout.Layout(
            crispy_forms.layout.HTML('<span class="tinfo">Address details are only necessary if there is going to be mail for users</span>'),
            crispy_forms.layout.HTML('<a class="btn btn-primary mb-3 ms-3" data-bs-toggle="collapse" \
                     href="#collapseAddress" role="button" aria-expanded="false" \
                     aria-controls="collapseAddress">Address details</a><br>'),
            crispy_forms.layout.Div(
                bootstrap5.FloatingField('address_line_1'),
                bootstrap5.FloatingField('address_line_2'),
                bootstrap5.FloatingField('parish'),
                bootstrap5.FloatingField('postcode'),
                css_class="collapse ps-3",
                id="collapseAddress"),
        )
        self.helper.form_id = 'id-profile-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'


# ENDPROFILE

# START POST AND COMMENTS

class ForumPostCreateForm(posts_and_comments_forms.PostCreateForm):
    class Meta(posts_and_comments_forms.PostCreateForm.Meta):
        model = forum_models.ForumPost
        fields = posts_and_comments_forms.PostCreateForm.Meta.fields + ['category', 'location']
        widgets = {'text': TinyMCE()}
        labels = {'category': 'Choose a category for your post...',
                  'location': 'Which island...?'}

    def __init__(self, user_name: str = None, post: forum_models.ForumPost = None, **kwargs) -> None:
        checked_string = ''
        super().__init__(**kwargs)
        if post and user_name and post.subscribed_users.filter(
                username=user_name).count():
            checked_string = 'checked'
        checkbox_string = '<input type="checkbox" id="subscribe_cb" name="subscribe" value="Subscribe" ' + \
            checked_string + '> \
                              <label for="subscribe_cb" class="tinfo">Subscribe to this post...</label><br>'
        self.helper.layout = crispy_forms.layout.Layout(
            crispy_forms.layout.Fieldset(
                'Create your post...',
                bootstrap5.FloatingField('title'),
                crispy_forms.layout.Field('text', css_class="mb-3 post-create-form-text"),
                crispy_forms.layout.HTML("<div class='font-italic mb-3 tinfo'>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</div>"),
                crispy_forms.layout.Div(Field('category', css_class="col-auto"), Field('location',
                    css_class="col-auto"), css_class="col-8 col-sm-4 col-md-4 col-lg-3 tinfo"),
                crispy_forms.layout.HTML(checkbox_string),
                crispy_forms.layout.Submit('save', 'Publish Post', css_class="col-auto mt-3 mb-3"),
            )
        )
        self.helper.form_action = 'django_forum:post_create_view'


class ForumCommentForm(posts_and_comments_forms.CommentForm):
    class Meta:
        model = forum_models.ForumComment
        fields = posts_and_comments_forms.CommentForm.Meta.fields + []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper.layout = crispy_forms.layout.Layout(
            crispy_forms.layout.Fieldset(
                '<h3 class="comment-headline">Comment away...!</h3>',
                crispy_forms.layout.Row(
                    crispy_forms.layout.Column(
                        crispy_forms.layout.Field('text', css_class="comment-form-text"),
                        crispy_forms.layout.Div(HTML('<span>...characters left: 500</span>'),
                            id="count", css_class="ms-auto tinfo"),
                        css_class="d-flex flex-column"),
                    css_class="d-flex flex-row align-items-end"),
                crispy_forms.layout.Submit('save', 'comment', css_class="col-auto mt-3"),
                css_class="tinfo")
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_forum:post_view'

## TODO add choices field to search page
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
    published = forms.ChoiceField(
        choices=PUBLISHED_CHOICES, required=False, initial=PUBLISHED_ANY)