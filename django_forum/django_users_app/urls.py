from django.urls import include, path
from .views import RegisterView, PasswordResetView
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls

urlpatterns = [
	path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
	#path('accounts/password_reset/', PasswordResetView.as_view(template_name='django_users_app/password_reset_form.html'), name='password_reset'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/', include(auth_urls)),

]