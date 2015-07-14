__author__ = 'Jeremy'

from django.conf.urls import patterns, url

from QianXun.manager.views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^login$', manager_login),
                       url(r'^password/reset$', manager_password_reset),
                       url(r'^school/notice$', view_upper_notice),
                       url(r'^canteen/notice$', view_canteen_notice),
                       url(r'^canteen/search$', cm_find_notice_by_keyword),
                       url(r'^school/search$', sm_find_notice_by_keyword),
                       url(r'^window$', view_window_info),
                       url(r'^permit$', permit_window),
                       url(r'^reject$', not_permit_window),
                       url(r'^create/canteen/notice$', cm_create_notice),
                       url(r'^modify/canteen/notice$', cm_modify_own_notice),
                       url(r'^delete/canteen/notice$', cm_delete_notice),
                       url(r'^create/school/notice$', sm_create_notice),
                       url(r'^modify/school/notice$', sm_modify_own_notice),
                       url(r'^delete/school/notice$', sm_delete_notice),

                       url(r'^school/windows$', get_all_school_windows),
                       url(r'^canteen/windows$', get_all_canteen_windows),

                       url(r'^window/search$', search_window_by_name),

                       url(r'window/dish$', show_window_dish),
                       )