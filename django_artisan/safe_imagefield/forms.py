from django import forms
from django.forms.widgets import ClearableFileInput

from .validators import AntiVirusValidator, FileContentTypeValidator, \
    FileExtensionValidator, MediaIntegrityValidator, MaxSizeValidator


class SafeImageField(forms.ImageField):
    def __init__(
            self,
            required=True,
            label='safe_image_field',
            initial=None,
            widget=ClearableFileInput,
            help_text='safe_image_field',
            **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.check_content_type = kwargs.pop('check_content_type', False)
        self.scan_viruses = kwargs.pop('scan_viruses', False)
        self.media_integrity = kwargs.pop('media_integrity', False)
        self.max_size_limit = kwargs.pop('max_size_limit', False)
        default_validators = []

        if self.allowed_extensions:
            default_validators.append(
                FileExtensionValidator(self.allowed_extensions)
            )

        if self.check_content_type:
            default_validators.append(FileContentTypeValidator())

        if self.scan_viruses:
            default_validators.append(AntiVirusValidator())

        if self.media_integrity:
            default_validators.append(MediaIntegrityValidator())

        if self.max_size_limit:
            default_validators.append(
                MaxSizeValidator(max_size=self.max_size_limit))

        self.default_validators = default_validators + self.default_validators

        super().__init__(**kwargs)

    def __clean__(self, value):
        # super().__clean__(value)
        self.cleaned_data = self.cleaned_data + super().clean()

        if self._errors:
            for error in self._errors:
                raise forms.ValidationError(str(error))
        else:
            return self.cleaned_data
