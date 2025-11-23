from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_injury, name='predict_injury'),
    path('health/', views.health_check, name='health_check'),
]

