__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.com_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^window/display/bycanteen$', common_window_display_bycanteen),
                       url(r'^window/display/byprotype$', common_window_display_byprotype),
)