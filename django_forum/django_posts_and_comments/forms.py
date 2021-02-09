from django.forms import ModelForm, CharField
from .models import Post, Comment
from tinymce.widgets import TinyMCE
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Fieldset, HTML, Div
from .fields import FloatingField
from crispy_forms.helper import FormHelper


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        widgets = { 'text':TinyMCE() }
        fields = ['title', 'text']
        labels = {
            'text': '',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Create your post...',
                FloatingField('title'),
                Field('text', css_class="mb-3", style="min-height:60vh"),
                HTML("<span>Maximum of 2000 characters.  Click on word count to see how many characters you have used...</span>"),
                Submit('save', 'Publish Post', css_class="col-3 mt-3"),
            )
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'post_create_view'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Comment away...!',
                Row(
                    Column(
                        Field('text', style="max-height:15vh"),
                        Div(HTML('<span>...characters left: 500</span>'), 
                            id="count", css_class="ms-auto"),
                               css_class="d-flex flex-column"),
                        css_class="d-flex flex-row"),
                Submit('save', 'comment', css_class="col-3 mt-3"),
            )
        )
        self.helper.form_id = 'id-post-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'post_create_view'
