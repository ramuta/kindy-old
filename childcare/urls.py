from django.conf.urls import patterns, url
from childcare import views
from classroom import views as classroom_views
from newsboard import views as newsboard_views

urlpatterns = patterns('',
                       #childcare
                       url(r'^$', views.childcare),
                       url(r'^managers/$', views.managers_list),

                       # classroom
                       url(r'^classroom/create/', classroom_views.classroom_create),

                       # diary
                       url(r'^diary/create/', classroom_views.diary_create),
                       url(r'^diary/(?P<diary_id>\d+)/$', classroom_views.diary_detail),
                       url(r'^diary/$', classroom_views.diary_section),
                       url(r'^diary/(?P<diary_id>\d+)/images/$', classroom_views.add_diary_images),

                       # newsboard
                       url(r'^newsboard/create/', newsboard_views.childcare_news_create),
                       url(r'^newsboard/(?P<news_id>\d+)/$', newsboard_views.childcare_news_detail),
                       url(r'^newsboard/$', newsboard_views.newsboard_section),

                       # newsboard
                       url(r'^page/create/', views.website_page_create),
                       url(r'^website/$', views.website_section),
                       url(r'^first-page/edit/', views.website_first_page_edit),
                       url(r'^theme/', views.website_choose_theme),

                       # gallery
                       url(r'^gallery/$', views.gallery_section),

                       # add users
                       url(r'^managers/add/$', views.managers_add_remove),
                       url(r'^employees/add/$', views.employees_add_remove),
                       )