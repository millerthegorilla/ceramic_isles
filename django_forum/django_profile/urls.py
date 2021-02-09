from django.urls import include, path
from .views import ProfileUpdateView


urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='profile_update_view'),
]