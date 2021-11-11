from crispy_forms import layout


class FloatingField(layout.Field):
    template = 'fields/profile_floating_field.html'


class FileInput(layout.Field):
    template = 'fields/profile_file_input.html'
