"""
URL configuration for injury_prediction project.
"""
from django.contrib import admin
from django.urls import path, include
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # Post-social-login success handler (issues token, redirects to SPA)
    path('accounts/social/success/', api_views.social_login_success, name='social_login_success'),
    # Provide explicit proxies for the Google provider so we can show a
    # helpful message if the provider isn't configured in the DB.
    path('accounts/google/login/', api_views.provider_google_login, name='provider_google_login'),
    path('accounts/google/login/callback/', api_views.provider_google_callback, name='provider_google_callback'),
    # Mount allauth routes (keep custom success handler above)
    path('accounts/', include('allauth.urls')),
]

