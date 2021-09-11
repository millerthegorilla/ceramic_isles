from django.conf import settings
from typing import Any, Dict


def navbarSpiel(request) -> Dict[str, Any]:
    return {'navbarSpiel': settings.NAVBAR_SPIEL}


def siteLogo(request) -> Dict[str, Any]:
    return {'siteLogo': settings.SITE_LOGO}
