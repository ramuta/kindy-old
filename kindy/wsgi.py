"""
WSGI config for kindy project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "kindy.settings"
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kindy.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application

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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'kindy.settings.local')
    application = get_wsgi_application()
else:
    from dj_static import Cling
    application = Cling(get_wsgi_application())
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
