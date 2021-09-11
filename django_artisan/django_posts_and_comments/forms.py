from django.forms import ModelForm, CharField, Form
from .models import Post, Comment
from tinymce.widgets import TinyMCE
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, HTML, Div
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        widgets = {'text': TinyMCE()}
        fields = ['title', 'text']
        labels = {
            'text': '',
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Create your post...',
                FloatingField('title'),
                Field(
                    'text',
                    css_class="mb-3 post-create-form-text"),
                HTML("<span>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</span>"),
                Submit(
                    'save',
                    'Publish Post',
                    css_class="col-3 mt-3"),
            ))
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_posts_and_comments:post_create_view'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
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
                Submit('save', 'comment', css_class="col-auto mt-3"), css_class="tinfo"
            )
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto mx-auto'
        self.helper.form_action = 'django_posts_and_comments:post_create_view'
