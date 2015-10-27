# -*- coding: UTF-8 -*-
from django.contrib import admin

from QianXun.orders.models import Promotions, Dish, OrdersDishes, Orders, DeliverTime


class MyModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class MyTabularInline(admin.TabularInline):
    def has_add_permission(self, request):
        return False


class DeliverTimeInline(MyTabularInline):
    """
    used by account.admin.WindowAdmin
    superuser can read windows' promotions
    """
    model = DeliverTime
    fieldsets = (
        (None, {
            'fields': ('date', 'time', 'is_valid',)
        }),
    )
    ordering = ('update_time',)
    readonly_fields = ('date', 'time', 'is_valid',)


class PromotionsInline(MyTabularInline):
    """
    used by account.admin.WindowAdmin
    superuser can read windows' promotions
    """
    model = Promotions
    fieldsets = (
        (None, {
            'fields': ('pro_type', 'rules', 'is_valid',)
        }),
    )
    ordering = ('update_time',)
    readonly_fields = ('pro_type', 'rules', 'is_valid',)


class DishInline(MyTabularInline):
    """
    used by account.admin.WindowAdmin
    superuser can read windows' dishes
    """
    model = Dish
    fieldsets = (
        (None, {
            'fields': ('dish_name', 'price', 'sales', 'grade', 'is_heat', 'description', 'is_valid',)
        }),
    )
    ordering = ('sales', 'update_time')
    readonly_fields = ('dish_name', 'price',  'sales', 'grade', 'is_heat', 'description',  'is_valid',)


class OrdersInline(MyTabularInline):
    """
    used by account.admin.CustomerAdmin
    superuser can read orders related to specific customer
    """
    model = Orders
    fieldsets = (
        (None, {
            'fields': ('order_id', 'window', 'building', 'address', 'show_dishes', 'promotion_list', 'discount',
                       'food_cost', 'deliver_cost', 'order_status',
                       'deliver_time', 'deal_time', 'notes', 'is_valid2customer', 'is_valid2window', )
        }),
    )
    ordering = ('update_time', )
    readonly_fields = ('order_id', 'window', 'building', 'address', 'show_dishes', 'promotion_list', 'discount',
                       'food_cost', 'deliver_cost', 'order_status',
                       'deliver_time', 'deal_time', 'notes', 'is_valid2customer', 'is_valid2window', )


class CommentInline(MyTabularInline):
    """
    used by DishAdmin
    superuser can read comments related to specific dish
    """
    model = OrdersDishes
    fieldsets = (
        (None, {
            'fields': ('orders', 'grade', 'text', 'comment_time', 'reply', 'reply_time',)
        }),
    )
    ordering = ('comment_time',)
    readonly_fields = ('orders', 'grade', 'text', 'comment_time', 'reply', 'reply_time')


class OrdersDishesInline(MyTabularInline):
    """
    used by OrdersAdmin
    superuser can read Dishes related to specific Order
    """
    model = OrdersDishes
    fieldsets = (
        (None, {
            'fields': ('dish', 'show_price', 'number', 'grade', 'text', 'comment_time', 'reply', 'reply_time')
        }),
    )
    ordering = ('dish', 'comment_time', )
    readonly_fields = ('dish', 'show_price', 'number', 'grade', 'text', 'comment_time', 'reply', 'reply_time')


class DeliverTimeAdmin(MyModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('window', 'date', 'show_time', 'is_valid', )
        }),
    )
    list_display = ('window', 'date', 'show_time', 'is_valid', 'update_time',)
    list_display_links = ('window',)
    list_filter = ('is_valid', 'update_time',)
    search_fields = ('window',)
    ordering = ('window', 'update_time',)
    readonly_fields = ('window', 'date', 'show_time', 'is_valid',)


class PromotionsAdmin(MyModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('window', 'pro_type', 'rules', 'is_valid')
        }),
    )
    list_display = ('rules', 'window',  'pro_type', 'is_valid', 'update_time')
    list_display_links = ('rules',)
    list_filter = ('is_valid', 'update_time', 'pro_type')
    search_fields = ('rules',)
    ordering = ('window', 'update_time',)
    readonly_fields = ('window', 'pro_type', 'rules', 'is_valid')


class DishAdmin(MyModelAdmin):
    inlines = [CommentInline, ]
    fieldsets = (
        (None, {
            'fields': ('window', 'dish_name', 'img_addr', 'price', 'grade', 'comment_number', 'sales', 'is_heat', 'description', 'is_valid')
        }),
    )
    list_display = ('dish_name', 'window',  'sales', 'is_valid', 'update_time')
    list_display_links = ('dish_name',)
    list_filter = ('is_valid', 'update_time',)
    search_fields = ('dish_name',)
    ordering = ('window', 'sales', 'update_time')
    readonly_fields = ('window', 'dish_name', 'img_addr', 'price', 'grade', 'comment_number', 'sales', 'is_heat', 'description', 'is_valid')

    def has_add_permission(self, request):
        return False

    def has_add_permission(self, request):
        return False


class OrdersAdmin(MyModelAdmin):
    inlines = [OrdersDishesInline]
    fieldsets = (
        (None, {
            'fields': ('order_id', 'window', 'customer', 'building', 'address',  'promotion_list', 'discount',
                       'food_cost', 'deliver_cost', 'order_status',
                       'deliver_time', 'deal_time', 'notes', 'is_valid2customer', 'is_valid2window')
        }),
    )
    list_display = ('window', 'customer', 'food_cost', 'order_status',
                    'is_valid2customer', 'is_valid2window', 'update_time')
    list_display_links = ('window',)
    list_filter = ('is_valid2customer', 'is_valid2window', 'update_time', 'order_status',)
    search_fields = ('window',)
    ordering = ('-update_time', )
    readonly_fields = ('order_id', 'window', 'customer', 'building', 'address',  'promotion_list', 'discount',
                       'food_cost', 'deliver_cost', 'order_status',
                       'deliver_time', 'deal_time', 'notes', 'is_valid2customer', 'is_valid2window')#'order_status',


admin.site.register(Promotions, PromotionsAdmin)
admin.site.register(DeliverTime, DeliverTimeAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Orders, OrdersAdmin)