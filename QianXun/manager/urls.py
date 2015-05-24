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
                       url(r'school/search$', sm_find_notice_by_keyword),
                       url(r'^window$', view_window_info),
                       url(r'^permit$', permit_window),
                       url(r'^notpermit$', not_permit_window),
                       )