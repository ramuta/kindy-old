from django.conf.urls import patterns, url
from childcare import views
from classroom import views as classroom_views
from newsboard import views as newsboard_views

urlpatterns = patterns('',
                       #childcare
                       url(r'^$', views.childcare),

                       # classroom
                       url(r'^classroom/create/$', classroom_views.classroom_create),
                       url(r'^classroom/$', classroom_views.classroom_list),
                       url(r'^classroom/(?P<classroom_id>\d+)/delete/$', classroom_views.classroom_delete),
                       url(r'^classroom/(?P<classroom_id>\d+)/update/$', classroom_views.classroom_update),

                       # diary
                       url(r'^diary/create/$', classroom_views.diary_create),
                       url(r'^diary/(?P<diary_id>\d+)/$', classroom_views.diary_detail),
                       url(r'^diary/$', classroom_views.diary_section),
                       url(r'^diary/(?P<diary_id>\d+)/images/$', classroom_views.add_diary_images),
                       url(r'^diary/(?P<diary_id>\d+)/delete/$', classroom_views.diary_delete),
                       url(r'^diary/(?P<diary_id>\d+)/update/$', classroom_views.diary_update),
                       url(r'^diary/(?P<diary_id>\d+)/image/(?P<image_id>\d+)/delete/$', classroom_views.diary_image_delete),

                       # newsboard
                       url(r'^newsboard/create/$', newsboard_views.childcare_news_create),
                       url(r'^newsboard/(?P<news_id>\d+)/$', newsboard_views.childcare_news_detail),
                       url(r'^newsboard/(?P<news_id>\d+)/images/$', newsboard_views.add_news_images),
                       url(r'^newsboard/(?P<news_id>\d+)/files/$', newsboard_views.add_news_files),
                       url(r'^newsboard/$', newsboard_views.newsboard_section),
                       url(r'^newsboard/(?P<news_id>\d+)/delete/$', newsboard_views.childcare_news_delete),
                       url(r'^newsboard/(?P<news_id>\d+)/update/$', newsboard_views.childcare_news_update),
                       url(r'^newsboard/(?P<news_id>\d+)/image/(?P<image_id>\d+)/delete/$', newsboard_views.news_image_delete),
                       url(r'^newsboard/(?P<news_id>\d+)/file/(?P<file_id>\d+)/delete/$', newsboard_views.news_file_delete),

                       # website
                       url(r'^page/create/$', views.website_page_create),
                       url(r'^pages/$', views.website_pages_list),
                       url(r'^page/(?P<page_id>\d+)/$', views.website_page_detail),
                       url(r'^page/(?P<page_id>\d+)/files/$', views.add_page_files),
                       url(r'^page/(?P<page_id>\d+)/delete/$', views.website_page_delete),
                       url(r'^page/(?P<page_id>\d+)/update/$', views.website_page_update),
                       url(r'^page/(?P<page_id>\d+)/file/(?P<file_id>\d+)/delete/$', views.page_file_delete),
                       url(r'^website/$', views.website_section),
                       url(r'^first-page/edit/$', views.website_first_page_edit),
                       url(r'^theme/$', views.website_choose_theme),

                       # gallery
                       url(r'^gallery/$', views.gallery_section),

                       # add users
                       url(r'^managers/add/$', views.managers_add_remove),
                       url(r'^employees/add/$', views.employees_add_remove),
                       url(r'^parents/add/$', views.parents_add_remove),

                       # users lists
                       url(r'^managers/$', views.managers_list),
                       url(r'^employees/$', views.employees_list),
                       url(r'^parents/$', views.parents_list),
                       )