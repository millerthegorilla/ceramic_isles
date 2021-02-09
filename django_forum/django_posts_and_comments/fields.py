from crispy_forms.layout import Field


# TODO: refactor the name FloatField to FloatingField so as not to clash with django model FloatField
class FloatingField(Field):
	template = 'fields/posts_and_comments_floating_field.html'


class FileInput(Field):
	template = 'fields/posts_and_comments_file_input.html'

