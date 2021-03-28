from crispy_forms.layout import Field


class FloatingField(Field):
    template = 'fields/users_app_floating_field.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["placeholder"] = self.fields[0]

class FileInput(Field):
    template = 'fields/users_app_file_input.html'