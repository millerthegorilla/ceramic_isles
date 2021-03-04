from django.urls import include, path
from .views import DashboardView, RegisterView, RulesPageView
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
	path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('rules/', RulesPageView.as_view(), name='rules_view')
]