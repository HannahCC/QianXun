# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from django import forms
from conf.enum_value import ORDER_STATUS, ORDER_BY
from QianXun.orders.models import Orders, Promotions, DeliverTime, Dish
from utils.Validator import validate_order_status, validate_customer_order_status, validate_window_order_status, \
    validate_pro_type, validate_image
from utils.Serializer import json_back

class OrderCalculateForm(forms.Form):
    token = forms.CharField(max_length=64)
    window = forms.IntegerField()
    food_cost = forms.FloatField()


class OrderDetailDisplayForm(forms.Form):
    token = forms.CharField(max_length=64)
    order = forms.IntegerField()


class OrderCreateForm(forms.ModelForm):
    token = forms.CharField(max_length=64)
    dish_list = forms.CharField(max_length=4096)

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Orders
        fields = ['window', 'promotion_list', 'discount', 'food_cost', 'deliver_cost',
                  'building', 'address', 'notes', 'deliver_time']

    def clean_address(self):
        cleaned_data = super(OrderCreateForm, self).clean()
        building = cleaned_data.get('building', '')
        address = cleaned_data.get('address', '')
        if not building and not address:
            raise forms.ValidationError(u'请输入楼栋ID或自定义地址ID')
        elif building and address:
            raise forms.ValidationError(u'请输入楼栋ID或自定义地址ID其中之一')
        return address

    def clean_dish_list(self):
        cleaned_data = super(OrderCreateForm, self).clean()
        dish_list_str = cleaned_data.get('dish_list', '')
        if not dish_list_str.startswith("[{") or not dish_list_str.endswith("}]"):
            raise forms.ValidationError(u'请输入json list格式的dish_list')
        else:
            dish_list = json_back(dish_list_str)
            for dish_json in dish_list:
                orders_dishes = dish_json.get('dish_id', '')
                if not isinstance(orders_dishes, int):
                    raise forms.ValidationError(u'请输入int型的dish_id')
                number = dish_json.get('number', '')
                if not isinstance(number, int):
                    raise forms.ValidationError(orders_dishes+u':请菜品的份数')
        return dish_list


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
    comment_list = forms.CharField(max_length=4096)

    def clean_comment_list(self):
        cleaned_data = super(CommentForm, self).clean()
        comment_list_str = cleaned_data.get('comment_list', '')
        if not comment_list_str.startswith("[{") or not comment_list_str.endswith("}]"):
            raise forms.ValidationError(u'请输入json list格式的comment_list')
        else:
            comment_list = json_back(comment_list_str)
            for comment_json in comment_list:
                orders_dishes = comment_json.get('orders_dishes', '')
                if not isinstance(orders_dishes, int):
                    raise forms.ValidationError(u'请输入int型的orders_dishes')
                grade = comment_json.get('grade', '')
                if not isinstance(orders_dishes, int) or grade < 1 or grade > 5:
                    raise forms.ValidationError(orders_dishes+u':请输入[1,5]范围的评分')
                text = comment_json.get('text', '')
                if not isinstance(text, unicode) or len(text) == 0:
                    raise forms.ValidationError(orders_dishes+u':评论不能为空')
        return comment_list


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


class DeleteIdListForm(forms.Form):
    token = forms.CharField(max_length=64)
    data = forms.CharField(max_length=4096)

    def clean_data(self):
        cleaned_data = super(DeleteIdListForm, self).clean()
        id_list_str = cleaned_data.get('data', '')
        if not id_list_str.startswith("[{") or not id_list_str.endswith("}]"):
            raise forms.ValidationError(u'请输入json list格式的id_list')
        else:
            id_list = json_back(id_list_str)
            for id_json in id_list:
                id = id_json.get('id', '')
                if not isinstance(id, int):
                    raise forms.ValidationError(u'请输入int型的id')
        return id_list