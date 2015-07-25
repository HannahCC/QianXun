__author__ = 'Jeremy'

from django.conf.urls import patterns, url

from QianXun.manager.views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^login$', manager_login),
                       url(r'^logout$', manager_logout),
                       url(r'^password/update$', manager_password_update),

                       url(r'^show/window/dish$', show_window_dish),
                       url(r'^show/school/notice$', mg_show_notice),
                       url(r'^search/school/notice$', mg_find_notice_by_keyword),

                       url(r'^show/canteen/notice$', cm_show_notice),
                       url(r'^search/canteen/notice$', cm_find_notice_by_keyword),
                       url(r'^create/canteen/notice$', cm_create_notice),
                       url(r'^modify/canteen/notice$', cm_modify_own_notice),
                       url(r'^delete/canteen/notice$', cm_delete_notice),
                       url(r'^show/canteen/window$', cm_get_canteen_windows),
                       url(r'^search/canteen/window$', cm_search_window_byname),
                       url(r'^verify/window$', cm_verify_window),

                       url(r'^create/school/notice$', sm_create_notice),
                       url(r'^modify/school/notice$', sm_modify_own_notice),
                       url(r'^delete/school/notice$', sm_delete_notice),
                       url(r'^show/school/window$', sm_get_school_windows),
                       url(r'^search/school/window$', sm_search_window_byname),


                       )