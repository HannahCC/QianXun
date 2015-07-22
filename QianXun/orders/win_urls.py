__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.orders.win_views import *


urlpatterns = patterns('',
                       url(r'^order/index$', index),
                       url(r'^promotion/create$', window_promotion_create),
                       url(r'^promotion/update$', window_promotion_update),
                       url(r'^promotion/delete$', window_promotion_delete),
                       url(r'^delivertime/create$', window_deliver_time_create),
                       url(r'^delivertime/update$', window_deliver_time_update),
                       url(r'^delivertime/delete$', window_deliver_time_delete),
                       url(r'^dish/create$', window_dish_create),
                       url(r'^dish/update$', window_dish_update),
                       url(r'^dish/delete$', window_dish_delete),
                       url(r'^order/display$', window_order_display),
                       url(r'^order/display/detail$', window_order_display_detail),
                       url(r'^order/update$', window_order_update),
                       url(r'^order/delete$', window_order_delete),
                       url(r'^comment/reply$', window_comment_reply),
                       url(r'^sales/dish$', window_sales_dish),
)