__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.orders.com_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^window/display/bycanteen$', common_window_display_bycanteen),
                       url(r'^window/display/byproname$', common_window_display_byproname),
                       url(r'^promotion/display/bywindow$', common_promotion_display_bywindow),
                       url(r'^promotion/display/byprotype', common_promotion_display_byprotype),
                       url(r'^delivertime/display/bywindow$', common_delivertime_display_bywindow),
                       url(r'^dish/display/bywindow$', common_dish_display_bywindow),
                       url(r'^dish/display/byname', common_dish_display_byname),
                       url(r'^comment/display/bydish$', common_comment_display_bydish),

)