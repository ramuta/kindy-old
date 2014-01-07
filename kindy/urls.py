import autocomplete_light
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from childcare import views as childcare_views
from django.conf import settings
from utils.deployment import is_local_env
from userena import views as userena_views

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
    url(r'^activate/(?P<activation_key>\w+)/$', userena_views.activate, {'success_url': '/'}, name='userena_activate'),

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

# check if app is local or deployed on server
LOCAL_ENV_BOOL = is_local_env()

if LOCAL_ENV_BOOL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)