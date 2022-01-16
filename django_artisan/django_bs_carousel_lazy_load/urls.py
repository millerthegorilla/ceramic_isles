from django.urls import path
from . import views as lazyload_views

app_name = "django_bs_carousel_lazy_load"

urlpatterns = [
	path('imgurl/<str:webp_support>/<str:screen_size>/<int:iteration>', 
		  lazyload_views.ImgURL.as_view(), name='img_url'),
]