from django.shortcuts import render_to_response

from utils.Decorator import token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response
from conf.resp_code import *
from forms import PaginationForm
from db import orderdish


def index(request):
    return render_to_response('test/testCommon.html')

@exception_handled
@token_required
@post_required
def common_district_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['school'] and request.POST['school'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        school_id = request.POST['school']
        district_bean_list = list.get_district_bean_list(school_id, pagination_dict)
        return json_response_from_object(OK, district_bean_list, 'district_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))

def common_window_display_bycanteen(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['canteen'] and request.POST['canteen'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        canteen_id = request.POST['canteen']

        district_bean_list = list.get_district_bean_list(school_id, pagination_dict)
        return json_response_from_object(OK, district_bean_list, 'district_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


def common_window_display_byproname(request):
    pass


def common_promotion_display_bywindow(request):
    pass


def common_promotion_display_byprotype(request):
    pass


def common_delivertime_display_bywindow(request):
    pass


def common_dish_display_bywindow(request):
    pass


def common_dish_display_byname(request):
    pass


@exception_handled
@token_required
@post_required
def common_comment_display_bydish(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['dish'] and request.POST['dish'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        dish_id = request.POST['dish']
        comment_bean_list = orderdish.get_comment_bean_list_bydish(dish_id, pagination_dict)
        return json_response_from_object(OK, comment_bean_list, 'comment_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
"""
    order_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': order_form})
"""

