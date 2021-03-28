from crispy_forms.layout import Field


class FloatingField(Field):
	template = 'fields/forum_app_floating_field.html'


class FileInput(Field):
	template = 'fields/forum_app_file_input.html'

