from django.conf.urls import patterns, url
from website import views

urlpatterns = patterns('',
                       url(r'^$', views.website),
                       url(r'^news/(?P<news_slug>[\w\-]+)/$', views.news_detail),
                       url(r'^news/$', views.website_news),
                       url(r'^(?P<page_slug>[\w\-]+)/$', views.page_detail),
                       )