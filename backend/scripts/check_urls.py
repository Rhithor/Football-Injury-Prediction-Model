import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injury_prediction.settings')
import django
from django.urls import resolve, Resolver404

django.setup()

paths = [
    '/accounts/google/login/',
    '/accounts/google/login/callback/',
    '/accounts/social/success/',
]

for p in paths:
    try:
        r = resolve(p)
        print(p, '->', getattr(r, 'view_name', r.func))
    except Resolver404:
        print(p, '-> NOT FOUND')
