from crispy_forms.layout import Field


class FloatingField(Field):
	template = 'fields/artisan_floating_field.html'


class FileInput(Field):
	template = 'fields/artisan_file_input.html'

