from django.contrib import admin

from QianXun.list.models import PromotionType, School, District, Building, Canteen


class PromotionTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('pro_type_name', 'is_valid', 'img_addr',)
        }),
    )
    list_display = ('pro_type_name', 'is_valid')
    list_display_links = ('pro_type_name',)
    list_filter = ('is_valid', 'update_time')
    search_fields = ('pro_type_name',)
    ordering = ('pro_type_name', 'update_time',)


class BuildingAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('building_name', 'terminal_id', 'district', 'is_valid',)
        }),
    )
    list_display = ('building_name', 'terminal_id', 'district',  'is_valid', 'update_time')
    list_display_links = ('building_name',)
    list_filter = ('is_valid', 'update_time')
    search_fields = ('building_name',)
    ordering = ('district', 'building_name', 'update_time',)


class DistrictAdmin(admin.ModelAdmin):
    # inlines = [BuildingInline, ]
    fieldsets = (
        (None, {
            'fields': ('district_name', 'school', 'is_valid',)
        }),
    )
    list_display = ('district_name', 'school',  'is_valid', 'update_time')
    list_display_links = ('district_name',)
    list_filter = ('is_valid', 'update_time', 'school',)
    search_fields = ('district_name',)
    ordering = ('school', 'district_name', 'update_time',)


class CanteenAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('canteen_name', 'school', 'is_valid', )
        }),
    )
    list_display = ('canteen_name', 'is_valid', 'update_time')
    list_display_links = ('canteen_name',)
    list_filter = ('is_valid', 'update_time', 'school',)
    search_fields = ('canteen_name',)
    ordering = ('school', 'canteen_name', 'update_time',)


class SchoolAdmin(admin.ModelAdmin):
    # inlines = (DistrictInline, CanteenInline)
    fieldsets = (
        (None, {
            'fields': ('school_name', 'is_valid',)
        }),
    )
    list_display = ('school_name', 'is_valid', 'update_time')
    list_display_links = ('school_name',)
    list_filter = ('is_valid', 'update_time')
    search_fields = ('school_name',)
    ordering = ('school_name', 'update_time',)


admin.site.register(PromotionType, PromotionTypeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Canteen, CanteenAdmin)
