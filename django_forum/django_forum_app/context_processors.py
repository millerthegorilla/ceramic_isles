from django.conf import settings

def app_name(request):
    return { 'app_name': settings.APP_NAME }

def navbar_spiel(request):
    return { 'navbar_spiel': settings.NAVBAR_SPIEL }
