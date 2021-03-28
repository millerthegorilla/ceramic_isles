from crispy_forms.layout import Field


class FloatingField(Field):
	template = 'fields/profile_floating_field.html'


class FileInput(Field):
	template = 'fields/profile_file_input.html'