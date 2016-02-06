# -*- coding: UTF-8 -*-
import sys
import os
from os.path import join, abspath, dirname

import environ

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

#from os import environ

def get_env_setting(setting):
	""" Get the environment setting or return exception """
	try:
		return environ[setting]
	except KeyError:
		error_msg = "Set the %s env variable" % setting
		raise ImproperlyConfigured(error_msg)


# PATH vars
# check if needed or not!
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

ROOT_DIR = environ.Path(__file__) - 2
env = environ.Env()


sys.path.insert(0, root('apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='mysupasiikrit')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Do not change this, set the ENV variable if you need to change the backend
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = env('EMAIL_PORT', default=25)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
DEFAULT_FROM_EMAIL = env('EMAIL_DEFAULT_FROM', default='noreply@example.com')


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'schedule',
    'happenings',
    'django_markdown',
)

PROJECT_APPS = (
    'hhlregistrations',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hhlevents.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hhlevents.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

import environ as djangoenviron
env = djangoenviron.Env()
if os.path.isfile('.env'):
    djangoenviron.Env.read_env('.env')
DATABASES = {
    'default': env.db("DATABASE_URL", default="postgres:///hhlevents"),
#     'default': djangoenviron.Env.db(var="", default="postgres:///hhlevents"),
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = (('fi', 'Finnish'),('en', 'English'),)
LOCALE_PATHS = ( PROJECT_ROOT + '/locale/', )

USE_I18N = True

TIME_ZONE = 'Europe/Helsinki'  # 'Europe/London'

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT_DIR('static'))

MEDIA_ROOT = root('assets', 'uploads')
MEDIA_URL = '/media/'

# Additional locations of static files

#STATICFILES_DIRS = (
#    root('assets'),
#)

TEMPLATE_DIRS = (
    root('templates'), 
)


HHLREGISTRATIONS_ROOT = root('apps/hhlregistrations/')


TEMPLATE_CONTEXT_PROCESSORS = (
    # Django defaults (NOTE: we should """Set the 'context_processors' option in the OPTIONS of a DjangoTemplates backend instead.""")
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # Other
    'django.core.context_processors.request',
    'hhlregistrations.context_processors.organisation_settings',
)

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary
if len(sys.argv) > 1 and 'test' in sys.argv[1]:
    from .testing import *
    

# Markdown settings
MARKDOWN_EDITOR_INIT_TEMPLATE = "base.html"

# messis.fi API
MESSIS_API_URL_GET_UPCOMING = "http://messis.fi/fi/?json=messis/get_upcoming_events"

# organisation_settings.py:
try:
    from .organisation_settings import *
except ImportError:
    print("importerror")
    pass
