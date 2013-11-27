from django.conf.urls import patterns, url
from childcare import views
from classroom import views as classroom_views
from newsboard import views as newsboard_views

urlpatterns = patterns('',
                       #childcare
                       url(r'^$', views.childcare),

                       # classroom
                       url(r'^classroom/create/', classroom_views.classroom_create),

                       # diary
                       url(r'^diary/create/', classroom_views.diary_create),
                       url(r'^diary/(?P<diary_id>\d+)/$', classroom_views.diary_detail),
                       url(r'^diary/$', classroom_views.diary_section),

                       # newsboard
                       url(r'^newsboard/create/', newsboard_views.childcare_news_create),
                       url(r'^newsboard/(?P<news_id>\d+)/$', newsboard_views.childcare_news_detail),
                       url(r'^newsboard/$', newsboard_views.newsboard_section),
                       )