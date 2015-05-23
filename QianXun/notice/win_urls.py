__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.notice.win_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^display$', window_notice_display),
                       url(r'^display/detail$', window_notice_display_detail),

)