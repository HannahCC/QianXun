__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.cus_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^registration$', customer_register),
                       url(r'^login$', customer_login),
                       url(r'^logout$', customer_logout),
                       url(r'^profile/display$', customer_profile_display),
                       url(r'^profile/update$', customer_profile_update),
                       url(r'^password/update$', customer_password_update),
                       url(r'^password/reset$', customer_password_reset),
                       url(r'^uname/reset$', customer_username_reset),
                       url(r'^feedback$', customer_feedback),
                       )