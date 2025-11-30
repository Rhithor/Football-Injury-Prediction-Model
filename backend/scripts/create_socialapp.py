"""Create a django-allauth SocialApp for Google using environment variables.

Usage: set GOOGLE_CLIENT_ID and GOOGLE_SECRET (and optionally SITE_ID)
then run: python backend/scripts/create_socialapp.py
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injury_prediction.settings')

try:
    import django
    django.setup()
except Exception as e:
    print('Django setup failed:', e)
    raise

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
SECRET = os.environ.get('GOOGLE_SECRET')
SITE_ID = int(os.environ.get('SITE_ID', os.environ.get('DJANGO_SITE_ID', '2')))

if not CLIENT_ID or not SECRET:
    print('Please set GOOGLE_CLIENT_ID and GOOGLE_SECRET environment variables.')
    sys.exit(1)

site = Site.objects.filter(id=SITE_ID).first()
if not site:
    print(f'Site with id={SITE_ID} not found. Available sites:')
    for s in Site.objects.all():
        print(f' {s.id} -> {s.domain} ({s.name})')
    sys.exit(1)

app, created = SocialApp.objects.get_or_create(provider='google', name='Google')
app.client_id = CLIENT_ID
app.secret = SECRET
app.save()

if not app.sites.filter(id=site.id).exists():
    app.sites.add(site)

print('SocialApp for google created/updated and attached to site:', site)
"""Create a django-allauth SocialApp for Google using environment variables.

Usage: set GOOGLE_CLIENT_ID and GOOGLE_SECRET (and optionally SITE_ID)
then run: python backend/scripts/create_socialapp.py
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'injury_prediction.settings')

try:
    import django
    django.setup()
except Exception as e:
    print('Django setup failed:', e)
    raise

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
SECRET = os.environ.get('GOOGLE_SECRET')
SITE_ID = int(os.environ.get('SITE_ID', os.environ.get('DJANGO_SITE_ID', '2')))

if not CLIENT_ID or not SECRET:
    print('Please set GOOGLE_CLIENT_ID and GOOGLE_SECRET environment variables.')
    sys.exit(1)

site = Site.objects.filter(id=SITE_ID).first()
if not site:
    print(f'Site with id={SITE_ID} not found. Available sites:')
    for s in Site.objects.all():
        print(f' {s.id} -> {s.domain} ({s.name})')
    sys.exit(1)

app, created = SocialApp.objects.get_or_create(provider='google', name='Google')
app.client_id = CLIENT_ID
app.secret = SECRET
app.save()

if not app.sites.filter(id=site.id).exists():
    app.sites.add(site)

print('SocialApp for google created/updated and attached to site:', site)
