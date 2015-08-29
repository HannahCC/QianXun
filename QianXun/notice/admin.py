# -*- coding:UTF-8 -*-
from django.contrib import admin

from QianXun.notice.models import SchoolNotice, CanteenNotice


class SchoolNoticeAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title', 'school', 'manager', 'content', 'is_valid',)
        }),
    )
    list_display = ('title', 'manager', 'is_valid', 'update_time',)
    list_display_links = ('title',)
    list_filter = ('is_valid', 'update_time', )
    search_fields = ('title',)
    ordering = ('update_time', 'title', )
    readonly_fields = ('title', 'school',  'manager', 'content', 'is_valid',)


class CanteenNoticeAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title', 'canteen',  'manager', 'content', 'is_valid',)
        }),
    )
    list_display = ('title', 'manager', 'is_valid', 'update_time',)
    list_display_links = ('title',)
    list_filter = ('is_valid', 'update_time', )
    search_fields = ('title',)
    ordering = ('update_time', 'title', )
    readonly_fields = ('title', 'canteen', 'manager', 'content', 'is_valid',)


admin.site.register(SchoolNotice, SchoolNoticeAdmin)
admin.site.register(CanteenNotice, CanteenNoticeAdmin)


