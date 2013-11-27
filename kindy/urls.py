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

    #childcare
    url(r'^childcare/create/$', childcare_views.childcare_create),
    url(r'^(?P<childcare_slug>[\w\-]+)/dashboard/', include('childcare.urls', namespace="childcare")),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)