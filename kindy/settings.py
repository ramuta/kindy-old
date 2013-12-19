# Django settings for kindy project.
import os
from utils.secret import get_secret_key

'''preverimo ali app tece lokalno ali na heroku
    na Heroku smo nastavili: heroku config:add DJANGO_LOCAL_DEV=0
'''
try:
    LOCAL_ENV = os.environ["DJANGO_LOCAL_DEV"]
    if LOCAL_ENV == 0 or LOCAL_ENV == '0':
        LOCAL_ENV_BOOL = False
    else:
        LOCAL_ENV_BOOL = True
except KeyError:
    LOCAL_ENV_BOOL = True

if LOCAL_ENV_BOOL:
    DEBUG = True
else:
    DEBUG = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

if LOCAL_ENV_BOOL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'database5.db',                      # Or path to database file if using sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd654pe0238l5dh',
            'USER': 'jbjfrmpkbkzixf',
            'PASSWORD': 'gH9qoFiE1XPhNPw_ztyJA8p9yZ',
            'HOST': 'ec2-54-204-45-126.compute-1.amazonaws.com',
            'PORT': '5432',
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

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
    os.path.join(DIRNAME, "static").replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

if LOCAL_ENV_BOOL:
    MEDIA_ROOT = os.path.join(DIRNAME, 'media/')
    MEDIA_URL = '/media/'
    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://example.com/media/", "http://media.example.com/"

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_ROOT = os.path.join(DIRNAME, 'staticfiles/')
    # ck editor
    CKEDITOR_UPLOAD_PATH = MEDIA_ROOT + 'ckeditor/'
else:
    AWS_STORAGE_BUCKET_NAME = 'getkindy'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL
    MEDIA_URL = S3_URL + 'media/'
    CKEDITOR_UPLOAD_PATH = 'ckeditor/'

# Make this unique, and don't share it with anybody.
# Nastavi env.variable na Heroku
if LOCAL_ENV_BOOL:
    SECRET_KEY = get_secret_key()
else:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

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

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)

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
    'autocomplete_light',
    'localflavor',
    'ckeditor',
    'south',
    'storages',
    'boto',

    'accounts',
    'childcare',
    'newsboard',
    'classroom',
    'website',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# emailing
if LOCAL_ENV_BOOL:
    # run in terminal: python -m smtpd -n -c DebuggingServer localhost:1025
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
else:  # TODO
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'yourgmailaccount@gmail.com'
    EMAIL_HOST_PASSWORD = 'yourgmailpassword'

# guardian
ANONYMOUS_USER_ID = -1
GUARDIAN_RENDER_403 = True

# auth and login
AUTH_PROFILE_MODULE = 'accounts.KindyUser'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'



CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 700,
    },
}

if not LOCAL_ENV_BOOL:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Allow all host headers
    ALLOWED_HOSTS = ['*']
    # Static asset configuration
    #import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #STATIC_ROOT = 'staticfiles'
    #STATIC_ROOT = 'staticfiles'
    #STATIC_URL = '/static/'
    '''STATICFILES_DIRS = (
        os.path.join(STATIC_ROOT, 'static'),
    )'''