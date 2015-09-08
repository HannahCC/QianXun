from QianXun import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = patterns('',
                       url(r'^qianxun/admin/', include(admin.site.urls)),
                       url(r'^qianxun/1/window/account/', include('QianXun.account.win_urls')),
                       url(r'^qianxun/1/window/notice/', include('QianXun.notice.win_urls')),
                       url(r'^qianxun/1/window/', include('QianXun.orders.win_urls')),

                       url(r'^qianxun/1/customer/account/', include('QianXun.account.cus_urls')),
                       url(r'^qianxun/1/customer/addr/', include('QianXun.account.cus_addr_urls')),
                       url(r'^qianxun/1/customer/', include('QianXun.orders.cus_urls')),

                       url(r'^qianxun/1/common/window/', include('QianXun.account.com_urls')),
                       url(r'^qianxun/1/common/verifycode/', include('QianXun.account.com_urls2')),
                       url(r'^qianxun/1/common/list/', include('QianXun.list.com_urls')),
                       url(r'^qianxun/1/common/', include('QianXun.orders.com_urls')),

                       url(r'^qianxun/1/manager/', include('QianXun.manager.urls')),
                       )
urlpatterns += patterns('',
                       url(r'^qianxun/img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT }),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT }),
                       url(r'^qianxun/template/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.TEMPLATE_ROOT }),
                       )
# urlpatterns += static(settings.TEMPLATE_URL, document_root=settings.TEMPLATE_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)