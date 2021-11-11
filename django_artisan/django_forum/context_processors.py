import typing

from django.conf import settings


def siteName(request) -> typing.Dict[str, str]:
    return {'siteName': settings.SITE_NAME}
