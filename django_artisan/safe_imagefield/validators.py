import mimetypes, os, logging

from django.core import exceptions
from django.utils import translation
from . import clamav, utils


logger = logging.getLogger('safe_imagefield')


# class FileNameValidator(object):
# TODO: check filename for double extensions
# https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
# lowercase all chars in filename
# check for hacks in filename as mentioned in link above
# ie check for double extensions or special chars in filename or strings such as 'php'
#  from the link :
#     All the control characters and Unicode ones should be removed from the filenames
#       and their extensions without any exception. Also, the special characters such as
#        “;”, “:”, “>”, “<”, “/” ,”\”, additional “.”, “*”, “%”, “$”, and so on should
#       be discarded as well.
#     It is recommended to use an algorithm to determine the filenames.
#       For instance, a filename can be a MD5 hash of the name of file plus the date
#       of the day.

# TODO do I need to call the superclass of object in each validator init??

class FileExtensionValidator(object):
    message = translation.ugettext_lazy(
        "File extension '%(extension)s' is not allowed. "
        "Allowed extensions are: '%(allowed_extensions)s'."
    )
    error_code = 'invalid_extension'

    def __init__(self, allowed_extensions=None, message=None, error_code=None) -> None:
        self.allowed_extensions = allowed_extensions

        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code

    def __call__(self, value):
        extension = os.path.splitext(value.name)[1][1:].lower()

        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            raise exceptions.ValidationError(
                self.message,
                code=self.error_code,
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(
                        self.allowed_extensions)
                }
            )


class FileContentTypeValidator(object):
    message = translation.ugettext_lazy(
        'File has invalid content-type. '
        'Maybe the file extension does not match the file content?'
    )

    error_code = 'invalid_content_type'

    def __init__(self, message=None, error_code=None) -> None:
        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code

    def __call__(self, file):
        __, ext = os.path.splitext(file.name)

        # TODO:  Update below code to match imagefile.
        detected_content_type = utils.detect_content_type(file)
        mimetypes.add_type('image/webp', '.webp', strict=True)
        if getattr(file, 'content_type', None) is not None:
            is_valid_content_type = bool(
                (
                    ext in mimetypes.guess_all_extensions(
                        detected_content_type)
                    and ext in mimetypes.guess_all_extensions(file.content_type)
                )
            )
            params = {
                'extension': ext,
                'content_type': file.content_type,
                'detected_content_type': detected_content_type
            }
        else:
            is_valid_content_type = bool(
                (
                    ext in mimetypes.guess_all_extensions(
                        detected_content_type)
                ) or (
                    detected_content_type == 'application/CDFV2-unknown'
                    and ext == "doc"
                )
            )
            params = {
                'extension': ext,
                'content_type': None,
                'detected_content_type': detected_content_type
            }

        if not is_valid_content_type:
            raise exceptions.ValidationError(
                self.message,
                code=self.error_code,
                params=params
            )


class AntiVirusValidator(object):
    message = translation.ugettext_lazy('File is infected with %(virus)s.')

    error_code = 'infected'

    def __init__(self, message=None, error_code=None) -> None:
        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code

    def __call__(self, file):
        status, virus_name = clamav.scan_file(file)
        if status != 'OK':
            raise exceptions.ValidationError(
                self.message,
                code=self.error_code,
                params={
                    'virus': virus_name
                }
            )


class MediaIntegrityValidator(object):
    # error_detect can be 'default' or 'strict'
    message = translation.ugettext_lazy('File failed integrity check! %(error)s')

    error_code = 'integrity_failure'

    def __init__(self, message=None, error_code=None, error_detect='default') -> None:
        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code

        self.error_detect = error_detect

    def __call__(self, file):
        content_type = utils.detect_content_type(file).split('/')[0]
        if content_type == 'video':
            utils.ffmpeg_check(file, self.error_detect)
        elif content_type == 'image':
            try:
                utils.pil_check(file)
            except Exception as e:
                logger.error("PIL CHECK ERROR : {0}".format(e))
                raise exceptions.ValidationError(
                    self.message, code=self.error_code, params={'error': str(e)})


class MaxSizeValidator(object):
    message = translation.ugettext_lazy('File is greater than %(max_size)s')

    error_code = 'max_size_error'

    def __init__(self, message=None, error_code=None, max_size=None) -> None:
        if message is not None:
            self.message = message

        if error_code is not None:
            self.error_code = error_code

        if max_size is not None:
            self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise exceptions.ValidationError(
                self.message, code=self.error_code, params={
                    'max_size': str(
                        utils.convert_size(
                            self.max_size))})
