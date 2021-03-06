# -*- coding: UTF-8 -*-
from django.contrib import admin

from QianXun.account.models import Window, Customer, Address
from QianXun.orders.admin import OrdersInline, PromotionsInline, DishInline, DeliverTimeInline


class MyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class MyTabularInline(admin.TabularInline):
    def has_add_permission(self, request):
        return False


class AddressInline(MyTabularInline):
    model = Address
    fieldsets = (
        (None, {
            'fields': ('customer', 'addr', 'is_valid', )
        }),
    )
    ordering = ('update_time', )
    readonly_fields = ('customer', 'addr', 'is_valid', )


class CustomerAdmin(MyModelAdmin):
    inlines = [AddressInline, OrdersInline]
    fieldsets = (
        (None, {
            'fields': ('user_name', 'nick_name','user_type', 'school', 'building',
                       'is_VIP', 'VIP_balance', 'VIP_deadline', 'is_valid', )
        }),
    )
    list_display = ('user_name', 'nick_name', 'user_type', 'school', 'is_valid', 'update_time',)
    list_display_links = ('user_name',)
    list_filter = ('is_valid', 'update_time', 'user_type', 'school', )
    search_fields = ('user_name',)
    ordering = ('school', 'user_name', 'update_time',)
    #list_per_page = 2
    readonly_fields = ('user_name', 'nick_name','user_type', 'school', 'building', 'is_valid')


class WindowAdmin(MyModelAdmin):
    inlines = [PromotionsInline, DeliverTimeInline, DishInline]
    fieldsets = (
        (None, {
            'fields': ('school', 'canteen', 'img_addr', 'window_name', 'window_status', 'grade', 'comment_number', 'sales', 'name', 'user_name', 'is_valid', )
        }),
    )
    list_display = ('window_name', 'name', 'user_name', 'window_status', 'canteen', 'sales', 'is_valid', 'update_time')
    list_display_links = ('window_name',)
    list_filter = ('is_valid', 'update_time', 'window_status')
    search_fields = ('window_name', 'user_name',)
    ordering = ('canteen', 'window_name', 'update_time',)
    readonly_fields = ('school', 'canteen', 'img_addr', 'window_name', 'grade', 'comment_number', 'sales', 'name', 'user_name', 'is_valid',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Window, WindowAdmin)
