from django.shortcuts import render_to_response

from utils.Decorator import token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response
from conf.resp_code import *
from forms import PaginationForm
from QianXun.account.db import window
from QianXun.orders.db import promotion


def index(request):
    return render_to_response('test/testCommon.html')


@exception_handled
@token_required
@post_required
def common_window_display_bycanteen(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['canteen'] and request.POST['canteen'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        canteen_id = request.POST['canteen']
        window_bean_list = window.get_window_bean_list_bycanteen(canteen_id, pagination_dict)
        return json_response_from_object(OK, window_bean_list, 'windowList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_window_display_byname(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['window_name'] and len(request.POST['window_name']) <= 64\
            and request.POST['school'] and request.POST['school'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        window_name = request.POST['window_name']
        school_id = request.POST['school']
        window_bean_list = window.get_window_bean_list_byname(school_id, window_name, pagination_dict)
        return json_response_from_object(OK, window_bean_list, 'windowList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_window_display_byprotype(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['pro_type'] and request.POST['pro_type'].isdigit() \
            and request.POST['school'] and request.POST['school'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        pro_type_id = request.POST['pro_type']
        school_id = request.POST['school']
        window_id_list = promotion.get_window_id_list_byprotype(school_id, pro_type_id, pagination_dict)
        window_bean_list = window.get_window_bean_list_byid(window_id_list)
        return json_response_from_object(OK, window_bean_list, 'windowList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))

"""
    order_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': order_form})
"""

