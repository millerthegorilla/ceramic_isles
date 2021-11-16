from crispy_forms import layout


# TODO: refactor the name FloatField to FloatingField so as not to clash
# with django model FloatField
class FloatingField(layout.Field):
    template = 'fields/posts_and_comments_floating_field.html'


class FileInput(layout.Field):
    template = 'fields/posts_and_comments_file_input.html'
