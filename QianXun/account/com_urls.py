__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.com_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^display/bycanteen$', common_window_display_bycanteen),
                       url(r'^display/byname$', common_window_display_byname),
                       url(r'^display/byprotype$', common_window_display_byprotype),
)