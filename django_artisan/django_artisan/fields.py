from django.forms import Form
from crispy_forms.layout import Field
from typing import Any


class FloatingField(Field):
    template = 'fields/artisan_floating_field.html'


class FileClearInput(Field):
    template = 'fields/artisan_file_clear_input.html'

    def render(
            self,
            form: Form,
            form_style: str,
            context: object,
            template_pack='bootstrap4',
            extra_context: object = None,
            **kwargs) -> Any:
        context['path'] = str(form['image_file'].value()).split('/')[-1]
        return super().render(
            form,
            form_style,
            context,
            template_pack,
            extra_context,
            **kwargs)


class FileInput(Field):
    template = 'fields/artisan_file_input.html'
