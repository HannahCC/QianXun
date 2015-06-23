# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from utils.Decorator import customer_token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response, json_back
from utils.MakeSerialNumber import new_order_id
from utils.CostCalculator import get_vip_discount, get_promotions_dict, get_promotions_discount, get_promotion_str_from_dict, get_deliver_cost
from utils.Push import JPush
from conf.resp_code import *
from conf.enum_value import ORDER_STATUS
from conf.default_value import ORDER_DISH_MAX, PROMOTION_MAX, NEW_ORDER_MSG
from forms import OrderCalculateForm, OrderCreateForm, OrderDetailDisplayForm, PaginationForm, CustomerOrderUpdateForm, \
    CommentForm, DeleteIdListForm
from db import promotion, order, orderdish
from QianXun.account.db import customer


def index(request):
    return render_to_response('test/testOrder.html')


@exception_handled
@customer_token_required
@post_required
def customer_order_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        customer_id = request.user_meta['customer_model'].id
        order_status = pagination_dict.get('order_status')
        order_bean_list = order.get_order_bean_list_bycus(customer_id, order_status, pagination_dict)
        return json_response_from_object(OK, order_bean_list, 'orderList')
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_order_display_detail(request):
    order_detail_display_form = OrderDetailDisplayForm(request.POST)
    if order_detail_display_form.is_valid():
        order_detail_display_dict = order_detail_display_form.cleaned_data
        customer_id = request.user_meta['customer_model'].id
        order_detail_bean = order.get_order_detail_byid_bycus(customer_id, order_detail_display_dict)
        return json_response_from_object(OK, order_detail_bean)
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@customer_token_required
@post_required
def customer_order_calculate(request):
    order_calculate_form = OrderCalculateForm(request.POST)
    if order_calculate_form.is_valid():
        customer_model = request.user_meta['customer_model']
        order_calculate_dict = order_calculate_form.cleaned_data
        window_id = order_calculate_dict['window']
        food_cost = order_calculate_dict['food_cost']
        deliver_cost = get_deliver_cost()
        discount = 0
        if customer.has_vip_balance(customer_model):    # customer is a valid VIP, and has VIP balance
            new_cost = get_vip_discount(food_cost)
            discount = food_cost - new_cost
            promotion_list = u"会员折扣"
        else:                                           # window has promotion_list
            promotion_list = promotion.get_promotion_list_bywindow(window_id, {'page': 1, 'count': PROMOTION_MAX})
            if len(promotion_list) > 0:
                promotions_dict = get_promotions_dict(food_cost, promotion_list)
                promotion_list = get_promotion_str_from_dict(promotions_dict)
                new_cost = get_promotions_discount(food_cost, promotions_dict)
                discount = food_cost - new_cost
        return json_response(OK, {'promotionList': promotion_list, 'discount': discount, 'deliver_cost': deliver_cost})
    else:
        return json_response(PARAM_REQUIRED, order_calculate_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_order_create(request):
    order_form = OrderCreateForm(request.POST)
    if order_form.is_valid():
        order_dict = order_form.cleaned_data
        dish_list = order_form['dish_list']
        if len(dish_list) <= ORDER_DISH_MAX:
            # initial the order_dict
            customer_model = request.user_meta['customer_model']
            order_dict.update({'customer': customer_model})
            window_id = order_dict['window'].id
            order_dict.update({'order_id': new_order_id(window_id)})
            my_order_model = order.create_bycus(order_dict)  # create a record in orders table,return a model with an id

            # add orders_dishes
            for dish_json in dish_list:
                orderdish.create(my_order_model.id, dish_json)
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(ORDER_DISH_REACH_MAX, CODE_MESSAGE.get(ORDER_DISH_REACH_MAX))
    else:
        return json_response(PARAM_REQUIRED, order_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_order_update(request):
    order_update_form = CustomerOrderUpdateForm(request.POST)
    if order_update_form.is_valid():
        order_update_dict = order_update_form.cleaned_data
        customer_id = request.user_meta['customer_model'].id
        impact = order.update_status_bycus(customer_id, order_update_dict)
        if impact == 1:
            if order_update_dict['new_order_status'] == ORDER_STATUS[1][0]:
                jpush = JPush()
                order_model = order.get_order_byid_bycus(customer_id, order_update_dict)
                registration_id = order_model.window.registration_id
                jpush.push_by_id(NEW_ORDER_MSG, registration_id)
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(DB_ERROR, CODE_MESSAGE.get(DB_ERROR))
    else:
        return json_response(PARAM_REQUIRED, order_update_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_order_delete(request):
    delete_id_list_form = DeleteIdListForm(request.POST)
    if delete_id_list_form.is_valid():
        delete_id_list_dict = delete_id_list_form.cleaned_data
        delete_id_list = delete_id_list_dict['data']
        customer_id = request.user_meta['customer_model'].id
        order_id_list_fail_to_delete = order.delete_bycus(customer_id, delete_id_list)
        return json_response_from_object(OK, order_id_list_fail_to_delete, 'orderIdList')
    else:
        return json_response(PARAM_REQUIRED, delete_id_list_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_comment_create(request):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_dict = comment_form.cleaned_data
        comment_list = comment_dict['comment_list']
        customer_id = request.user_meta['customer_model'].id
        my_order = order.get_order_byid_bycus(customer_id, comment_dict)
        if my_order.order_status == ORDER_STATUS[7][0]:  # user can only make comment on order in 'ready to comment'
            for comment_json in comment_list:
                orderdish.update_comment(my_order, comment_json)
            # update the status of my_order
            order_update_dict = {'order': my_order.id, 'old_order_status': ORDER_STATUS[7][0],
                                 'new_order_status': ORDER_STATUS[8][0]}
            order.update_status_bycus(customer_id, order_update_dict)
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(ORDER_STATUS_ERROR, CODE_MESSAGE.get(ORDER_STATUS_ERROR))
    else:
        return json_response(PARAM_REQUIRED, comment_form.errors)


