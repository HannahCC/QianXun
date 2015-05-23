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
def comment_display_bydish(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid() and request.POST['dish']:
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

