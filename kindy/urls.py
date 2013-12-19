import os
import autocomplete_light
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from childcare import views as childcare_views

autocomplete_light.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # home
    url(r'^$', 'kindy.views.home', name='home'),

    # accounts
    url(r'^accounts/', include('userena.urls')),

    #autocomplete
    url(r'autocomplete/', include('autocomplete_light.urls')),

    #ckeditor
    url(r'^ckeditor/', include('ckeditor.urls')),

    #childcare
    url(r'^childcare/create/$', childcare_views.childcare_create),
    url(r'^(?P<childcare_slug>[\w\-]+)/dashboard/', include('childcare.urls', namespace="childcare")),

    #website
    url(r'^(?P<childcare_slug>[\w\-]+)/', include('website.urls', namespace="website")),
)

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

if LOCAL_ENV_BOOL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)