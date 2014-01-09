from django.conf.urls import patterns, url
from childcare import views
from classroom import views as classroom_views
from newsboard import views as newsboard_views

urlpatterns = patterns('',
                       #childcare
                       url(r'^childcare/$', views.childcare, name='childcare_info'),
                       url(r'^childcare/update/$', views.childcare_update, name='childcare_update'),

                       #users
                       url(r'^childcare/users/invite/$', views.invite_users, name='invite_users'),
                       url(r'^childcare/managers/(?P<username>[\w\-]+)/remove/$', views.remove_manager, name='manager_remove'),
                       url(r'^childcare/employees/(?P<username>[\w\-]+)/remove/$', views.remove_employee, name='employee_remove'),
                       url(r'^childcare/parents/(?P<username>[\w\-]+)/remove/$', views.remove_parent, name='parent_remove'),
                       url(r'^childcare/managers/$', views.managers_list, name='manager_list'),
                       url(r'^childcare/employees/$', views.employees_list, name='employee_list'),
                       url(r'^childcare/parents/$', views.parents_list, name='parent_list'),
                       #url(r'^childcare/users/$', views.users_list, name='user_list'),

                       # classroom
                       url(r'^classroom/create/$', classroom_views.classroom_create, name='classroom_create'),
                       url(r'^classroom/$', classroom_views.classroom_list, name='classroom_list'),
                       url(r'^classroom/(?P<classroom_id>\d+)/delete/$', classroom_views.classroom_delete, name='classroom_delete'),
                       url(r'^classroom/(?P<classroom_id>\d+)/update/$', classroom_views.classroom_update, name='classroom_update'),

                       # diary
                       url(r'^diary/create/$', classroom_views.diary_create, name='diary_create'),
                       url(r'^diary/(?P<diary_id>\d+)/$', classroom_views.diary_detail, name='diary_detail'),
                       url(r'^diary/$', classroom_views.diary_section, name='diary_list'),
                       url(r'^diary/(?P<diary_id>\d+)/images/$', classroom_views.add_diary_images, name='diary_add_images'),
                       url(r'^diary/(?P<diary_id>\d+)/delete/$', classroom_views.diary_delete, name='diary_delete'),
                       url(r'^diary/(?P<diary_id>\d+)/update/$', classroom_views.diary_update, name='diary_update'),
                       url(r'^diary/(?P<diary_id>\d+)/image/(?P<image_id>\d+)/delete/$', classroom_views.diary_image_delete, name='diary_image_delete'),

                       # newsboard
                       url(r'^newsboard/create/$', newsboard_views.childcare_news_create, name='news_create'),
                       url(r'^newsboard/(?P<news_id>\d+)/$', newsboard_views.childcare_news_detail, name='news_detail'),
                       url(r'^newsboard/(?P<news_id>\d+)/images/$', newsboard_views.add_news_images, name='news_add_images'),
                       url(r'^newsboard/(?P<news_id>\d+)/files/$', newsboard_views.add_news_files, name='news_add_files'),
                       url(r'^newsboard/$', newsboard_views.newsboard_section, name='news_list'),
                       url(r'^newsboard/(?P<news_id>\d+)/delete/$', newsboard_views.childcare_news_delete, name='news_delete'),
                       url(r'^newsboard/(?P<news_id>\d+)/update/$', newsboard_views.childcare_news_update, name='news_update'),
                       url(r'^newsboard/(?P<news_id>\d+)/image/(?P<image_id>\d+)/delete/$', newsboard_views.news_image_delete, name='news_image_delete'),
                       url(r'^newsboard/(?P<news_id>\d+)/file/(?P<file_id>\d+)/delete/$', newsboard_views.news_file_delete, name='news_file_delete'),

                       # website
                       url(r'^website/page/create/$', views.website_page_create, name='page_create'),
                       url(r'^website/$', views.website_pages_list, name='page_list'),
                       url(r'^website/page/(?P<page_id>\d+)/files/$', views.add_page_files, name='page_add_files'),
                       url(r'^website/page/(?P<page_id>\d+)/delete/$', views.website_page_delete, name='page_delete'),
                       url(r'^website/page/(?P<page_id>\d+)/update/$', views.website_page_update, name='page_update'),
                       url(r'^website/page/(?P<page_id>\d+)/file/(?P<file_id>\d+)/delete/$', views.page_file_delete, name='page_file_delete'),
                       url(r'^website/page/about/edit/$', views.website_first_page_edit, name='about_edit'),
                       url(r'^website/theme/$', views.website_choose_theme, name='choose_theme'),

                       # gallery
                       url(r'^gallery/$', views.gallery_section, name='gallery'),
                       )