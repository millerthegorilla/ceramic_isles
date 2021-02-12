from django.urls import include, path
from .views import ProfileUpdateView, ProfileUpLoadView

app_name="django_profile"
urlpatterns = [
    path('profile/images/update/', ProfileUploadView.as_view(), name='image_update'),
    path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/images/update/<slug:unique_id>/', ProfileImageDeleteView.as_view(), name='remove_images')
]