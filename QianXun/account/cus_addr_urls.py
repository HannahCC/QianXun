__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.cus_views import *


urlpatterns = patterns('',
                       url(r'^display$', customer_addr_display),
                       url(r'^create$', customer_addr_create),
                       url(r'^update$', customer_addr_update),
                       url(r'^delete$', customer_addr_delete),
                       url(r'^custom/display$', customer_custom_addr_display),
                       url(r'^custom/create$', customer_custom_addr_create),
                       url(r'^custom/update$', customer_custom_addr_update),
                       url(r'^custom/delete$', customer_custom_addr_delete),
                       )