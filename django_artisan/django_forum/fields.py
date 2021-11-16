from crispy_forms import layout


class FloatingField(layout.Field):
    template = 'fields/forum_app_floating_field.html'


class FileInput(layout.Field):
    template = 'fields/forum_app_file_input.html'
