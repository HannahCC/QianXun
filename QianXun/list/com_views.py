from django.shortcuts import render_to_response

from utils.Decorator import token_required, post_required, exception_handled
from utils.Serializer import json_response_from_object, json_response
from conf.resp_code import *
from forms import PaginationForm
from db import list


def index(request):
    return render_to_response('test/testCommon.html')


@exception_handled
@token_required
@post_required
def common_school_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        school_bean_list = list.get_school_bean_list(pagination_dict)
        return json_response_from_object(OK, school_bean_list, 'school_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


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


@exception_handled
@token_required
@post_required
def common_building_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['district'] and request.POST['district'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        district_id = request.POST['district']
        building_bean_list = list.get_building_bean_list(district_id, pagination_dict)
        return json_response_from_object(OK, building_bean_list, 'building_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_canteen_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['school'] and request.POST['school'].isdigit():
        pagination_dict = pagination_form.cleaned_data
        school_id = request.POST['school']
        canteen_bean_list = list.get_canteen_bean_list(school_id, pagination_dict)
        return json_response_from_object(OK, canteen_bean_list, 'canteen_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@token_required
@post_required
def common_protype_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        pro_type_bean_list = list.get_protype_bean_list(pagination_dict)
        return json_response_from_object(OK, pro_type_bean_list, 'pro_type_list')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))

"""
    order_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': order_form})
"""

