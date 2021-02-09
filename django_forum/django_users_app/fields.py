from crispy_forms.layout import Field


class FloatingField(Field):
	template = 'fields/users_app_floating_field.html'


class FileInput(Field):
	template = 'fields/users_app_file_input.html'