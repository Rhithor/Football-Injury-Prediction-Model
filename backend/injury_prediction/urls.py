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
    # Endpoint used after social login completes - issues token and redirects to frontend
    path('accounts/social/success/', api_views.social_login_success, name='social_login_success'),
    # Include allauth routes after custom success route so our handler is reachable
    path('accounts/', include('allauth.urls')),
]

