from django import urls
from . import views as profile_views

app_name = "django_profile"
urlpatterns = [
    urls.path('', profile_views.ProfileUpdate.as_view(), name='profile_update_view'),
]

# NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegister
# path('users/accounts/register/', CustomRegister.as_view(), name='register'),
