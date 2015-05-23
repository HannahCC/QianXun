# -*- coding: UTF-8 -*-
from django.contrib import admin

from QianXun.manager.models import SchoolManager, CanteenManager


class SchoolManagerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'user_name', 'school', 'is_valid',)
        }),
    )
    list_display = ('user_name', 'name', 'school', 'is_valid', 'update_time')
    list_display_links = ('user_name',)
    list_filter = ('is_valid', 'update_time', 'school')
    search_fields = ('user_name', 'name', )
    ordering = ('school', 'user_name',)


class CanteenManagerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'user_name', 'canteen', 'is_valid',)
        }),
    )
    list_display = ('user_name', 'name', 'canteen', 'is_valid', 'update_time')
    list_display_links = ('user_name',)
    list_filter = ('is_valid', 'update_time', )
    search_fields = ('user_name', 'name', )
    ordering = ('canteen', 'user_name',)


admin.site.register(SchoolManager, SchoolManagerAdmin)
admin.site.register(CanteenManager, CanteenManagerAdmin)