"""
Django settings for atlas_project project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# import django_python3_ldap

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1244ztx296$iq9s3peaw3y8ab@h9i-3q$sher8or68_#7^)x=c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

local_apps = [
    'entry.apps.EntryConfig',
    'home.apps.HomeConfig',
    'charts.apps.ChartsConfig',
]

default_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

third_party_apps = [
    'crispy_forms',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    # 'channels',
]

INSTALLED_APPS = local_apps + default_apps + third_party_apps

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'atlas_project.authentication_middleware.AutomaticUserLoginMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'django_python3_ldap.auth.LDAPBackend',
    # 'atlas_project.authentication_backend.AuthenticationBackend',
]

ROOT_URLCONF = 'atlas_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'atlas_project.wsgi.application'

# # For simple usernames (e.g. "username"):
# LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"

# # For down-level login name formats (e.g. "DOMAIN\username"):
# # LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
# # LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "DOMAIN"

# # For user-principal-name formats (e.g. "user@domain.com"):
# # LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"
# # LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "domain.com"

# LDAP_AUTH_USER_FIELDS = {
#     "username": "username",
#     "first_name": "personfirstname",
#     "last_name": "personlastname",
#     "email": "email",
# }

# LDAP_AUTH_OBJECT_CLASS = "user"

# # For debugging purposes, remove this part once application is ready for production

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django_python3_ldap": {
#             "handlers": ["console"],
#             "level": "INFO",
#         },
#     },
# }


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DBSCHEMA'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
        'HOST': os.environ.get('DBHOST'),
        'PORT': os.environ.get('DBPORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

DATETIME_INPUT_FORMATS = ['%d/%m/%Y %I:%M %p', ]

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_ID')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
