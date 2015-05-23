from django.shortcuts import render_to_response

from utils.Decorator import token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response
from conf.resp_code import *
from forms import PaginationForm
from db import window


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
        return json_response_from_object(OK, window_bean_list, 'window_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


def common_window_display_byprotype(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['pro_type'] and request.POST['pro_type'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        pro_type_id = request.POST['pro_type']
        window_bean_list = window.get_window_bean_list_byprotype(pro_type_id, pagination_dict)
        return json_response_from_object(OK, window_bean_list, 'window_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))

"""
    order_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': order_form})
"""

