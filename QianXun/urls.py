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

                       url(r'^qianxun/1/common/window/', include('QianXun.account.com_urls')),
                       url(r'^qianxun/1/common/list/', include('QianXun.list.com_urls')),
                       url(r'^qianxun/1/common/', include('QianXun.orders.com_urls')),



                       )
