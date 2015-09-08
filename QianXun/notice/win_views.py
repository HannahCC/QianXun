from django.shortcuts import render_to_response

from QianXun.utils.Decorator import window_token_required, post_required, exception_handled
from QianXun.utils.Serializer import json_response, json_response_from_object
from conf.resp_code import *
from QianXun.notice.forms import PaginationForm, NoticeDetailDisplayForm
from db import notice

# Create your views here.


def index(request):
    return render_to_response('test/testNotice.html')


@exception_handled
@window_token_required
@post_required
def window_notice_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        window_model = request.user_meta['window_model']
        canteen_notice_bean_list = notice.get_canteen_notice_bean_list_bycanteen(window_model.canteen, pagination_dict)
        return json_response_from_object(OK, canteen_notice_bean_list, 'noticeList')
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@window_token_required
@post_required
def window_notice_display_detail(request):
    notice_detail_display_form = NoticeDetailDisplayForm(request.POST)
    if notice_detail_display_form.is_valid():
        notice_detail_display_form = notice_detail_display_form.cleaned_data
        window_model = request.user_meta['window_model']
        canteen_notice_detail_bean = notice.get_canteen_notice_detail_bean_byid(window_model.canteen, notice_detail_display_form)
        return json_response_from_object(OK, canteen_notice_detail_bean)
    else:
        return json_response(PARAM_REQUIRED, notice_detail_display_form.errors)

"""
    promotion_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': promotion_form})
"""