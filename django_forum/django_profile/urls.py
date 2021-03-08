from django.urls import include, path
from .views import ProfileUpdateView, CustomRegisterView

app_name="django_profile"
urlpatterns = [
    path('', ProfileUpdateView.as_view(), name='profile_update_view'),
]

### NEEDED FOR ADDITION OF DISPLAY_NAME
# the following goes in the project top level urls.py
# from django_profile.views import CustomRegisterView
# path('users/accounts/register/', CustomRegisterView.as_view(), name='register'),