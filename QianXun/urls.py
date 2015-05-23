from django.conf.urls import patterns, include, url
from django.contrib import admin
from orders import com_views
urlpatterns = patterns('',
                       url(r'^qianxun/admin/', include(admin.site.urls)),
                       url(r'^qianxun/1/window/account/', include('QianXun.account.win_urls')),
                       url(r'^qianxun/1/window/notice/', include('QianXun.notice.win_urls')),
                       url(r'^qianxun/1/window/', include('QianXun.orders.win_urls')),

                       url(r'^qianxun/1/customer/account/', include('QianXun.account.cus_urls')),
                       url(r'^qianxun/1/customer/addr/', include('QianXun.account.cus_addr_urls')),
                       url(r'^qianxun/1/customer/', include('QianXun.orders.cus_urls')),


                       url(r'^qianxun/1/common/index$', com_views.index),
                       url(r'^qianxun/1/comment/display/bydish$', com_views.comment_display_bydish),

                       url(r'^qianxun/1/manager/', include('QianXun.manager.urls')),
                       )
