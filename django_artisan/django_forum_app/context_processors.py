from django.conf import settings

def siteName(request):
    return { 'siteName': settings.SITE_NAME }
