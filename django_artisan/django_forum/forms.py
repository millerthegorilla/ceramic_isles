from collections import namedtuple
from datetime import datetime, timedelta, timezone

from crispy_forms import helper, layout
from crispy_bootstrap5 import bootstrap5 
from tinymce.widgets import TinyMCE

from django import forms, utils
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from django_profile import forms as profile_forms
from django_messages import forms as messages_forms

from . import models as forum_models


# START FORUMPROFILE
# class AvatarForm(forms.Form):
#     def __init__(*args, **kwargs):


class ForumProfileUser(profile_forms.ProfileUser):
    class Meta(profile_forms.ProfileUser.Meta):
        fields = profile_forms.ProfileUser.Meta.fields
        model = profile_forms.ProfileUser.Meta.model

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
        self.helper.layout = layout.Layout(
            bootstrap5.FloatingField('display_name'),
            self.helper.layout)


class ForumProfile(profile_forms.Profile):
    class Meta(profile_forms.Profile.Meta):
        model = forum_models.ForumProfile
        fields = profile_forms.Profile.Meta.fields + [
            'address_line_1',
            'address_line_2',
            'parish',
            'postcode',
        ]
        exclude = ['profile_user']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.HTML('<span class="tinfo">Address details are only necessary if there is going to be mail for users</span>'),
            layout.HTML('<a class="btn btn-primary mb-3 ms-3" data-bs-toggle="collapse" \
                     href="#collapseAddress" role="button" aria-expanded="false" \
                     aria-controls="collapseAddress">Address details</a><br>'),
            layout.Div(
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

class ForumPost(messages_forms.Message):
    class Meta(messages_forms.Message.Meta):
        model = forum_models.ForumPost
        fields = messages_forms.Message.Meta.fields + ['title']
        widgets = {'text': TinyMCE()}
        labels = {'category': 'Choose a category for your post...',
                  'location': 'Which island...?'}

    def __init__(self, user_name: str = None, post: forum_models.ForumPost = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
        self.helper.form_action = 'django_forum:post_create_view'


class ForumComment(messages_forms.Message):
    class Meta:
        model = forum_models.ForumComment
        fields = messages_forms.Message.Meta.fields

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                '<h3 id="comment" class="comment-headline">Comment away...!</h3>',
                layout.Row(
                    layout.Column(
                        layout.Field('text', css_class="comment-form-text"),
                        layout.Div(layout.HTML('<span>...characters left: 500</span>'),
                            id="count", css_class="ms-auto tinfo"),
                        css_class="d-flex flex-column"),
                    css_class="d-flex flex-row align-items-end"),
                layout.Submit('save', 'comment', css_class="col-auto mt-3"),
                css_class="tinfo")
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_forum:post_view'

## TODO add choices field to search page
class ForumPostListSearch(forms.Form):
    date_end_of_last_month = datetime(utils.timezone.now().year, utils.timezone.now().month, 1) - timedelta(1)
    DATE_ANY = 0
    DATE_TODAY = (utils.timezone.now(), datetime(utils.timezone.now().year, 
                                                 utils.timezone.now().month, 
                                                 utils.timezone.now().day, 0, 0, 0))
    DATE_WEEK = (utils.timezone.now(), utils.timezone.now() - timedelta(7))
    DATE_WEEK_LAST = (utils.timezone.now() - timedelta(7), utils.timezone.now() - timedelta(14))
    DATE_MONTH_LAST = (datetime(utils.timezone.now().year, utils.timezone.now().month - 1, 
                                date_end_of_last_month.day, tzinfo=timezone.utc),
                       datetime(utils.timezone.now().year, utils.timezone.now().month - 1, 
                                1, tzinfo=timezone.utc))
    DATE_YEAR_NOW = (utils.timezone.now(), datetime(utils.timezone.now().year, 1, 1, tzinfo=timezone.utc))
    DATE_YEAR_LAST = (datetime(utils.timezone.now().year - 1, 12, 31, tzinfo=timezone.utc), 
                      datetime(utils.timezone.now().year - 1, 1, 1, tzinfo=timezone.utc))


    #from dateparser import parse  TODO add search verbs to allow time phrases to be passed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DATES = {}
        self.DATES['DATE_ANY'] = self.DATE_ANY
        self.DATES['DATE_TODAY'] = self.DATE_TODAY
        self.DATES['DATE_WEEK'] = self.DATE_WEEK
        self.DATES['DATE_WEEK_LAST'] = self.DATE_WEEK_LAST
        self.DATES['DATE_MONTH_LAST'] = self.DATE_MONTH_LAST
        self.DATES['DATE_YEAR_NOW'] = self.DATE_YEAR_NOW
        self.DATES['DATE_YEAR_LAST'] = self.DATE_YEAR_LAST

    DATE_CHOICES = (
        ('DATE_ANY', 'Any'),
        ('DATE_TODAY', 'Today'),
        ('DATE_WEEK', 'This week'),
        ('DATE_WEEK_LAST', 'A week ago'),
        ('DATE_MONTH_LAST', 'Last month'),
        ('DATE_YEAR_NOW', 'This year'),
        ('DATE_YEAR_LAST', 'Last year'),
    )

    q = forms.CharField(label='Search Query')
    published = forms.ChoiceField(choices=DATE_CHOICES, required=False, initial=DATE_ANY)
    
    class Meta():
        fields = []