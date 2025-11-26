"""
Django settings for injury_prediction project.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',
]

SITE_ID = 2
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'injury_prediction.middleware.AuthDebugMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'injury_prediction.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'injury_prediction.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# During local development enable debug logging so our auth middleware prints
# messages to the console. This is intentionally minimal and only applies when
# DEBUG=True.
if DEBUG:
    import logging

    logging.basicConfig(level=logging.DEBUG)

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

REST_AUTH = {
    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
}

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Prefer using SocialApp configured in the Django admin (database) for
# OAuth credentials. If you *do* want to configure the provider via
# settings instead, add the APP config here and remove the SocialApp
# entry from the admin to avoid duplicates which cause MultipleObjectsReturned
# errors when allauth finds more than one app for the same provider.
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # DO NOT include an 'APP' key here if you've created a SocialApp
        # record in the Django admin. Keep scope and auth params in settings
        # while storing client_id/secret on the SocialApp database object.
        'SCOPE': ['profile', 'email'],
        # Allow configuring the Google OAuth prompt via environment so
        # different environments can choose different UX (e.g., 'login' to
        # force password entry, 'select_account' to show chooser, or
        # 'consent' to force the consent screen).
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': config('GOOGLE_OAUTH_PROMPT', default='login')
        },
    }
}

# Force manual signup for social accounts so users must finish the site's
# registration form instead of auto-provisioning. This prevents accidental
# auto-creation and ensures users have a username on the site.
# When True, django-allauth will automatically create a local user account
# when a social account provides sufficient information (e.g. an email).
# Set to False to force users to complete the site's signup form (manual)
# before an account is created.
SOCIALACCOUNT_AUTO_SIGNUP = False

# Use a debug adapter to log social login events during development
SOCIALACCOUNT_ADAPTER = 'api.adapters.DebugSocialAccountAdapter'

# After successful login (including social), redirect to an internal success view
# that issues a token and then redirects the user to the frontend with the token
LOGIN_REDIRECT_URL = '/accounts/social/success/'
SOCIALACCOUNT_LOGIN_REDIRECT_URL = '/accounts/social/success/'
LOGOUT_REDIRECT_URL = 'http://localhost:5173/'

# Frontend base url used when redirecting back after certain auth flows.
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')