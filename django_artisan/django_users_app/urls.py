from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls

from .views import RegisterView, ResendConfirmationView
from .forms import UserPasswordResetForm

urlpatterns = [
	path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
	path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='django_users_app/resend_form.html', form_class=UserPasswordResetForm, extra_context={'instructions':'Send a password reset link...'}), name='password_reset'),
    path('accounts/resend_confirmation/', ResendConfirmationView.as_view(), name='resend_confirmation'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/', include(auth_urls)),
]