import os

execfile(os.path.join(os.path.dirname(__file__), "site_settings.py"))

TEMPLATE_DEBUG = DEBUG

ADMINS = ((PHOTOGRAPHER_NAME, PHOTOGRAPHER_EMAIL),)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), "tzadik.db")
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

LANGUAGE_CODE = 'en-us'
USE_I18N = False

MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "media")
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin-media/"

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(__file__), "templates")
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.sessions',
    'photoblog'
]
