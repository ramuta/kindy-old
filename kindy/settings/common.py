import os
from logentries import LogentriesHandler

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html


LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
DIRNAME = os.path.dirname(__file__)

'''
MEDIA_ROOT = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'
'''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, "../static").replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

THUMBNAIL_ALIASES = {
    'newsboard.NewsImage.image': {
        'thumb': {
            'size': (100, 100),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },

    'classroom.DiaryImage.image': {
        'thumb': {
            'size': (100, 100),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'kindy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'kindy.wsgi.application'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../../', 'templates').replace('\\','/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'userena',
    'guardian',
    'easy_thumbnails',
    'widget_tweaks',
    'localflavor',
    'south',
    'storages',
    'boto',
    'logentries',
    'celery',
    'redis',
    'billiard',
    'kombu',
    'accounts',
    'childcare',
    'newsboard',
    'classroom',
    'website',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# guardian
ANONYMOUS_USER_ID = -1
GUARDIAN_RENDER_403 = True

# auth and login
AUTH_PROFILE_MODULE = 'accounts.KindyUser'
#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
USERENA_SIGNIN_REDIRECT_URL = '/'