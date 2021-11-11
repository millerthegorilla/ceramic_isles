from django import urls
from . import views as profile_views

app_name = "django_profile"
urlpatterns = [
    urls.path('', profile_views.ProfileUpdateView.as_view(), name='profile_update_view'),
]

# NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegisterView
# path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),
