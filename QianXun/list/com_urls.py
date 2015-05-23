__author__ = 'Hannah'
from django.conf.urls import patterns, url

from QianXun.list.com_views import *


urlpatterns = patterns('',
                       url(r'^index$', index),
                       url(r'^school/display$', common_school_display),
                       url(r'^district/display$', common_district_display),
                       url(r'^building/display$', common_building_display),
                       url(r'^canteen/display$', common_canteen_display),
                       url(r'^protype/display$', common_protype_display),

)