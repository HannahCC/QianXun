# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from django import forms
from conf.enum_value import ORDER_STATUS, ORDER_BY
from QianXun.orders.models import Orders, Promotions, DeliverTime, Dish
from utils.Validator import validate_order_status, validate_customer_order_status, validate_window_order_status, \
    validate_pro_type, validate_image


class OrderForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Orders
        fields = ['window']


class OrderDetailDisplayForm(forms.Form):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()


class OrderConfirmForm(forms.ModelForm):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(OrderConfirmForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Orders
        fields = ['building', 'address', 'notes', 'deliver_time']

    def clean_address(self):
        cleaned_data = super(OrderConfirmForm, self).clean()
        building = cleaned_data.get('building', '')
        address = cleaned_data.get('address', '')
        if not building and not address:
            raise forms.ValidationError(u'请输入楼栋ID或自定义地址ID')
        elif building and address:
            raise forms.ValidationError(u'请输入楼栋ID或自定义地址ID其中之一')
        return address


class OrderUpdateForm(forms.Form):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()
    new_order_status = forms.ChoiceField(choices=ORDER_STATUS)
    old_order_status = forms.ChoiceField(choices=ORDER_STATUS)

    def clean_old_order_status(self):
        cleaned_data = super(OrderUpdateForm, self).clean()
        new_order_status = cleaned_data.get('new_order_status', '')
        old_order_status = cleaned_data.get('old_order_status', '')
        if not validate_order_status(old_order_status, new_order_status):
            raise forms.ValidationError(u'请输入合法的订单状态<逻辑错误>')
        return old_order_status


class CustomerOrderUpdateForm(OrderUpdateForm):
    def __init__(self, *args, **kwargs):
        super(CustomerOrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['new_order_status'].validators.append(validate_customer_order_status)


class WindowOrderUpdateForm(OrderUpdateForm):
    def __init__(self, *args, **kwargs):
        super(WindowOrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['new_order_status'].validators.append(validate_window_order_status)


class CommentForm(forms.Form):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()
    orders_dishes = forms.IntegerField()
    grade = forms.FloatField(min_value=1, max_value=5)
    text = forms.CharField(min_length=1, max_length=64)


class ReplyForm(forms.Form):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()
    orders_dishes = forms.IntegerField()
    reply = forms.CharField(min_length=1, max_length=64)


class PromotionForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Promotions
        fields = ['pro_type', 'rules']

    def clean_rules(self):
        cleaned_data = super(PromotionForm, self).clean()
        pro_type = cleaned_data.get('pro_type', '')
        rules = cleaned_data.get('rules', '')
        if not validate_pro_type(pro_type, rules):
            raise forms.ValidationError(u'请输入合法的活动规则')
        return rules


class PromotionUpdateForm(PromotionForm):
    promotion = forms.IntegerField()


class DeliverTimeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(DeliverTimeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DeliverTime
        fields = ['date', 'time']


class DeliverTimeUpdateForm(DeliverTimeForm):
    deliver_time = forms.IntegerField()


class DishForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields['img_addr'].validators.append(validate_image)

    class Meta:
        model = Dish
        fields = ['dish_name', 'price', 'is_heat', 'description', 'img_addr']


class DishUpdateForm(DishForm):
    dish = forms.IntegerField()


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)
    order_status = forms.ChoiceField(choices=ORDER_STATUS, required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY, required=False)


class SalesForm(forms.Form):
    token = forms.CharField(max_length=64)
    start_date = forms.DateField()
    end_date = forms.DateField()