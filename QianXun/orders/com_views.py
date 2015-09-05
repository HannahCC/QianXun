from django.shortcuts import render_to_response

from utils.Decorator import token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response
from conf.resp_code import *
from conf.enum_value import ORDER_BY
from forms import PaginationForm
from QianXun.orders.db import promotion, deliver_time, dish, orderdish, order
from QianXun.account.db import customer, window, verifycode
from QianXun.notice.db import notice

def index(request):
    return render_to_response('test/testCommon.html')


@exception_handled
@token_required
@post_required
def common_promotion_display_bywindow(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['window'] and request.POST['window'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        window_id = request.POST['window']
        promotion_bean_list = promotion.get_promotion_bean_list_bywindow(window_id, pagination_dict)
        return json_response_from_object(OK, promotion_bean_list, 'promotionList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_delivertime_display_bywindow(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['window'] and request.POST['window'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        window_id = request.POST['window']
        deliver_time_bean_list = deliver_time.get_deliver_time_bean_list_bywindow(window_id, pagination_dict)
        return json_response_from_object(OK, deliver_time_bean_list, 'deliverTimeList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_dish_display_bywindow(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and 'order_by' in request.POST \
            and 'window' in request.POST and request.POST['window'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        window_id = request.POST['window']
        order_by = ORDER_BY[int(request.POST['order_by'])][1]
        dish_bean_list = dish.get_dish_bean_list_bywin(window_id, pagination_dict, order_by)
        return json_response_from_object(OK, dish_bean_list, 'dishList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_dish_display_byname(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and 'order_by' in request.POST \
            and 'dish_name' in request.POST and len(request.POST['dish_name']) <= 64\
            and 'school' in request.POST and request.POST['school'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        dish_name = request.POST['dish_name']
        school_id = request.POST['school']
        order_by = ORDER_BY[int(request.POST['order_by'])][1]
        dish_bean_list = dish.get_dish_bean_list_byname(school_id, dish_name, pagination_dict, order_by)
        return json_response_from_object(OK, dish_bean_list, 'dishList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_comment_display_bydish(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and 'dish' in request.POST and request.POST['dish'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        dish_id = request.POST['dish']
        comment_bean_list = orderdish.get_comment_bean_list_bydish(dish_id, pagination_dict)
        return json_response_from_object(OK, comment_bean_list, 'commentList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
def common_delete_all(request):
    dish_number = dish.delete_all()
    deliver_time_number = deliver_time.delete_all()
    promotion_number = promotion.delete_all()
    orderdish_number = orderdish.delete_all()
    order_number = order.delete_all()
    customer_number = customer.delete_all()
    window_number = window.delete_all()
    verifycode_number = verifycode.delete_all()

    result = {'dish_number':dish_number,
    'deliver_time_number':deliver_time_number,
    'promotion_number':promotion_number,
    'orderdish_number':orderdish_number,
    'order_number':order_number,
    'customer_number':customer_number,
    'window_number':window_number,
    'verifycode_number':verifycode_number}
    return json_response(OK, result)
