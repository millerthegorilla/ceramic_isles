from tinymce import widgets
from crispy_forms import layout, helper
from crispy_bootstrap5 import bootstrap5

from django import forms

from . import models as posts_and_comments_models


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = posts_and_comments_models.Post
        widgets = {'text': widgets.TinyMCE()}
        fields = ['title', 'text']
        labels = {
            'text': '',
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Create your post...',
                bootstrap5.FloatingField('title'),
                layout.Field(
                    'text',
                    css_class="mb-3 post-create-form-text"),
                layout.HTML("<span>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</span>"),
                layout.Submit(
                    'save',
                    'Publish Post',
                    css_class="col-3 mt-3"),
            ))
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_posts_and_comments:post_create_view'


class CommentForm(forms.ModelForm):
    class Meta:
        model = posts_and_comments_models.Comment
        fields = ['text']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Comment away...!',
                layout.Row(
                    layout.Column(
                        layout.Field('text', css_class="comment-form-text"),
                        layout.Div(HTML('<span>...characters left: 500</span>'),
                            id="count", css_class="ms-auto tinfo"),
                        css_class="d-flex flex-column"),
                    css_class="d-flex flex-row align-items-end"),
                layout.Submit('save', 'comment', css_class="col-auto mt-3"), css_class="tinfo"
            )
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto mx-auto'
        self.helper.form_action = 'django_posts_and_comments:post_create_view'
