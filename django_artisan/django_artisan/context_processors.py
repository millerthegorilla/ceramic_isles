from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest

def navbarSpiel(request: HttpRequest) -> Dict[str, Any]:
    return {'navbarSpiel': settings.NAVBAR_SPIEL}


def siteLogo(request: HttpRequest) -> Dict[str, Any]:
    return {'siteLogo': settings.SITE_LOGO}
