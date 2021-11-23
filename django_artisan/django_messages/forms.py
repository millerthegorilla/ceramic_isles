from crispy_forms import layout, helper
from crispy_bootstrap5 import bootstrap5

from django import forms

from . import models as messages_models


class Message(forms.ModelForm):
    class Meta:
        model = messages_models.Message
        fields = ['text',]
        # labels = {
        #     'text': '',
        # }

    def __init__(self, *args, **kwargs) -> None:
        breakpoint()
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                'Create your message...',
                bootstrap5.FloatingField('title'),
                layout.Field(
                    'text',
                    css_class="mb-3 message-create-form-text"),
                layout.Submit(
                    'save',
                    'Save Message',
                    css_class="col-3 mt-3"),
            ))
        self.helper.form_id = 'id-message-create-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'col-auto'
        self.helper.form_action = 'django_messages:message_create'
