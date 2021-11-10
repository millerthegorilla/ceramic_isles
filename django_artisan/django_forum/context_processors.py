from django.conf import settings
from typing import Any, Dict


def siteName(request) -> Dict[str, Any]:
    return {'siteName': settings.SITE_NAME}
