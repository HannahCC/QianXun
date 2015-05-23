__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.orders.cus_views import *


urlpatterns = patterns('',
                       url(r'^order/index$', index),
                       url(r'^order/create$', customer_order_create),
                       url(r'^order/display$', customer_order_display),
                       url(r'^order/display/detail$', customer_order_display_detail),
                       url(r'^order/confirm$', customer_order_confirm),
                       url(r'^order/update$', customer_order_update),
                       url(r'^order/delete$', customer_order_delete),
                       url(r'^comment/create$', customer_comment_create),
                       )