from django.conf import settings

def navbarSpiel(request):
    return { 'navbarSpiel': settings.NAVBAR_SPIEL }

def siteLogo(request):
	return { 'siteLogo': settings.SITE_LOGO }
