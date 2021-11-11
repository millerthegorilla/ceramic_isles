from crispy_forms import layout


class FloatingField(layout.Field):
    template = 'fields/users_app_floating_field.html'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.attrs["placeholder"] = self.fields[0]


class FileInput(layout.Field):
    template = 'fields/users_app_file_input.html'
