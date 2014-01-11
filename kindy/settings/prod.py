from common import *
import os
#import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = DEBUG

'''
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
'''



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
        },
        'logentries_handler':{
            'token': os.environ["LOGENTRIES_TOKEN"],
            'class': 'logentries.LogentriesHandler'
        },
    },
        'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'logentries': {
            'handlers': ['logentries_handler'],
            'level': 'INFO',
        },
    }
}

AWS_STORAGE_BUCKET_NAME = 'getkindy'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
AWS_PRELOAD_METADATA = False
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_QUERYSTRING_AUTH = False

# Make this unique, and don't share it with anybody.
# Nastavi env.variable na Heroku
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# emailing
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@getkindy.com'
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD"]

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))