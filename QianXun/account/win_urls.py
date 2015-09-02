__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.win_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^registration$', window_register),
                       url(r'^login$', window_login),
                       url(r'^logout$', window_logout),
                       url(r'^profile/display$', window_profile_display),
                       url(r'^profile/update$', window_profile_update),
                       url(r'^profile/image/update$', window_profile_image_update),
                       url(r'^password/update$', window_password_update),
                       url(r'^password/reset$', window_password_reset),
                       url(r'^uname/reset$', window_username_reset),
                       url(r'^feedback$', window_feedback),
)