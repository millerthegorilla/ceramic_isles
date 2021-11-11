import typing

from django import forms
from django.db import models
from django.utils.deconstruct import deconstructible

from . import forms as safe_image_forms
from . import validators


class SafeImageField(models.ImageField):
    def __init__(self, allowed_extensions=None, check_content_type=False,
                 scan_viruses=False, media_integrity=False, *args, **kwargs) -> None:
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.check_content_type = kwargs.pop('check_content_type', False)
        self.scan_viruses = kwargs.pop('scan_viruses', False)
        self.media_integrity = kwargs.pop('media_integrity', False)
        self.max_size_limit = kwargs.pop('max_size_limit', False)
        default_validators = []

        if self.allowed_extensions:
            default_validators.append(
                typing.cast(object, validators.FileExtensionValidator(self.allowed_extensions))
            )

        if self.check_content_type:
            default_validators.append(cast(object, validators.FileContentTypeValidator()))

        if self.scan_viruses:
            default_validators.append(cast(object, validators.AntiVirusValidator()))

        if self.media_integrity:
            default_validators.append(cast(object, validators.MediaIntegrityValidator()))

        if self.max_size_limit:
            default_validators.append(
                cast(object, validators.MaxSizeValidator(max_size=self.max_size_limit)))

        self.default_validators = default_validators + self.default_validators

        super().__init__(**kwargs)

    def formfield(self, **kwargs) -> forms.Field:
        return super().formfield(
            form_class=safe_image_forms.SafeImageField
        )

    def __eq__(self, other: 'SafeImageField'):
        if (self.allowed_extensions == other.allowed_extensions and 
                self.check_content_type == other.check_content_type and 
                self.scan_viruses == other.scan_viruses):
            return True
        else:
            return False

    def deconstruct(self) -> typing.Tuple[str, str, list[typing.Any], dict[str, typing.Any]]:
        name, path, args, kwargs = super().deconstruct()
        kwargs['allowed_extensions'] = self.allowed_extensions
        kwargs['check_content_type'] = self.check_content_type
        kwargs['scan_viruses'] = self.scan_viruses
        kwargs['media_integrity'] = self.media_integrity
        kwargs['max_size_limit'] = self.max_size_limit
        return (name, path, args, kwargs)
