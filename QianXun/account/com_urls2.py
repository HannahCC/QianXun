__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.account.com_views import *


urlpatterns = patterns('',
                       url(r'^validation$', common_verifycode_validation),
)