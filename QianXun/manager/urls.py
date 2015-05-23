__author__ = 'Jeremy'

from django.conf.urls import patterns, url

from QianXun.manager.views import *


urlpatterns = patterns('',
                       url(r'index$', index),
                       url(r'login$', manager_login),
                       )