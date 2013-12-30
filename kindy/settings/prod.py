from common import *
import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG

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

AWS_STORAGE_BUCKET_NAME = 'getkindy'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
AWS_PRELOAD_METADATA = False
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
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
DATABASES['default'] = dj_database_url.config()
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
