from django.shortcuts import render_to_response

from QianXun.utils.Decorator import window_token_required, post_required, exception_handled
from QianXun.utils.Serializer import json_response, json_response_from_object
from QianXun.utils.SalesStat import stat_window_sales
from conf.resp_code import *
from conf.default_value import PROMOTION_MAX, DELIVER_TIME_MAX, DISH_MAX
from conf.enum_value import ORDER_STATUS
from forms import PaginationForm, PromotionForm, PromotionUpdateForm, DeliverTimeForm, DeliverTimeUpdateForm, DishForm, \
    DishUpdateForm, DishUpdateImageForm, OrderDetailDisplayForm, WindowOrderUpdateForm, ReplyForm, SalesForm, DeleteIdListForm
from QianXun.orders.db import promotion, deliver_time, dish, order, orderdish
from QianXun.account.db import window

def index(request):
    return render_to_response('test/testOrder.html')


@exception_handled
@window_token_required
@post_required
def window_promotion_create(request):
    promotion_form = PromotionForm(request.POST)
    if promotion_form.is_valid():
        window_model = request.user_meta['window_model']
        if window_model.promotion_number <= PROMOTION_MAX:
            new_promotion = promotion.create(promotion_form, False)
            new_promotion.window = window_model
            promotion_bean = promotion.create(new_promotion)
            window.update_promotion_number(window_model, 1)  # update promotion_number of window
            window.update_promotion_list(window_model)
            return json_response_from_object(OK, promotion_bean)
        else:
            return json_response(PROMOTION_REACH_MAX, CODE_MESSAGE.get(PROMOTION_REACH_MAX))
    else:
        return json_response(PARAM_REQUIRED, promotion_form.errors)


@exception_handled
@window_token_required
@post_required
def window_promotion_update(request):
    promotion_update_form = PromotionUpdateForm(request.POST)
    if promotion_update_form.is_valid():
        window_model = request.user_meta['window_model']
        promotion_update_dict = promotion_update_form.cleaned_data
        impact = promotion.update(window_model.id, promotion_update_dict)
        if impact == 1:
            window.update_promotion_list(window_model)
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(DB_ERROR, CODE_MESSAGE.get(DB_ERROR))
    else:
        return json_response(PARAM_REQUIRED, promotion_update_form.errors)


@exception_handled
@window_token_required
@post_required
def window_promotion_delete(request):
    delete_id_list_form = DeleteIdListForm(request.POST)
    if delete_id_list_form.is_valid():
        delete_id_list_dict = delete_id_list_form.cleaned_data
        delete_id_list = delete_id_list_dict['data']
        window_model = request.user_meta['window_model']
        promotion.delete(window_model.id, delete_id_list)
        window.update_promotion_number(window_model, -1)  # update promotion_number of window
        window.update_promotion_list(window_model)
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, delete_id_list_form.errors)


@exception_handled
@window_token_required
@post_required
def window_deliver_time_create(request):
    deliver_time_form = DeliverTimeForm(request.POST)
    if deliver_time_form.is_valid():
        window_model = request.user_meta['window_model']
        if window_model.deliver_time_number <= DELIVER_TIME_MAX:
            new_deliver_time = deliver_time.create(deliver_time_form, False)
            new_deliver_time.window = window_model
            deliver_time_bean = deliver_time.create(new_deliver_time)
            window.update_deliver_time_number(window_model, 1)  # update deliver_time_number of window
            return json_response_from_object(OK, deliver_time_bean)
        else:
            return json_response(DELIVER_TIME_REACH_MAX, CODE_MESSAGE.get(DELIVER_TIME_REACH_MAX))
    else:
        return json_response(PARAM_REQUIRED, deliver_time_form.errors)


@exception_handled
@window_token_required
@post_required
def window_deliver_time_update(request):
    deliver_time_updated_form = DeliverTimeUpdateForm(request.POST)
    if deliver_time_updated_form.is_valid():
        deliver_time_updated_dict = deliver_time_updated_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        impact = deliver_time.update(window_id, deliver_time_updated_dict)
        if impact == 1:
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(DB_ERROR, CODE_MESSAGE.get(DB_ERROR))
    else:
        return json_response(PARAM_REQUIRED, deliver_time_updated_form.errors)


@exception_handled
@window_token_required
@post_required
def window_deliver_time_delete(request):
    delete_id_list_form = DeleteIdListForm(request.POST)
    if delete_id_list_form.is_valid():
        delete_id_list_dict = delete_id_list_form.cleaned_data
        delete_id_list = delete_id_list_dict['data']
        window_model = request.user_meta['window_model']
        deliver_time.delete(window_model.id, delete_id_list)
        window.update_deliver_time_number(window_model, -1)  # update deliver_time_number of window
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, delete_id_list_form.errors)


@exception_handled
@window_token_required
@post_required
def window_dish_create(request):
    dish_form = DishForm(request.POST, request.FILES)
    if dish_form.is_valid():
        window_model = request.user_meta['window_model']
        if window_model.dish_number <= DISH_MAX:
            new_dish = dish.create(dish_form, False)
            new_dish.window = window_model
            dish_bean = dish.create(new_dish)
            window.update_dish_number(window_model, 1)  # update dish_number of window
            return json_response_from_object(OK, dish_bean)
        else:
            return json_response(DISH_REACH_MAX, CODE_MESSAGE.get(DISH_REACH_MAX))
    else:
        return json_response(PARAM_REQUIRED, dish_form.errors)


@exception_handled
@window_token_required
@post_required
def window_dish_update(request):
    dish_update_form = DishUpdateForm(request.POST, request.FILES)
    if dish_update_form.is_valid():
        dish_update_dict = dish_update_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        impact = dish.update(window_id, dish_update_dict)
        if impact == 1:
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(DB_ERROR, CODE_MESSAGE.get(DB_ERROR))
    else:
        return json_response(PARAM_REQUIRED, dish_update_form.errors)


@exception_handled
@window_token_required
@post_required
def window_dish_image_update(request):
    dish_update_form = DishUpdateImageForm(request.POST, request.FILES)
    if dish_update_form.is_valid():
        dish_update_dict = dish_update_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        dish_model = dish.update_image(window_id, dish_update_dict)
        result = {"ImgAddr": str(dish_model.img_addr)}
        return json_response(OK, result)
    else:
        return json_response(PARAM_REQUIRED, dish_update_form.errors)


@exception_handled
@window_token_required
@post_required
def window_dish_delete(request):
    delete_id_list_form = DeleteIdListForm(request.POST)
    if delete_id_list_form.is_valid():
        delete_id_list_dict = delete_id_list_form.cleaned_data
        delete_id_list = delete_id_list_dict['data']
        window_model = request.user_meta['window_model']
        dish.delete(window_model.id, delete_id_list)
        window.update_dish_number(window_model, -1)  # update dish_number of window
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, delete_id_list_form.errors)


@exception_handled
@window_token_required
@post_required
def window_order_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        order_status = pagination_dict['order_status']
        if not order_status == ORDER_STATUS[0][0]:
            order_bean_list = order.get_order_bean_list_bywin(window_id, order_status, pagination_dict)
            return json_response_from_object(OK, order_bean_list, 'orderList')
        else:
            return json_response(ORDER_STATUS_ERROR, CODE_MESSAGE.get(ORDER_STATUS_ERROR))
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@window_token_required
@post_required
def window_order_display_detail(request):
    order_detail_display_form = OrderDetailDisplayForm(request.POST)
    if order_detail_display_form.is_valid():
        order_detail_display_dict = order_detail_display_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        order_detail_bean = order.get_order_detail_byid_bywin(window_id, order_detail_display_dict)
        return json_response_from_object(OK, order_detail_bean)
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@window_token_required
@post_required
def window_order_update(request):
    order_update_form = WindowOrderUpdateForm(request.POST)
    if order_update_form.is_valid():
        order_update_dict = order_update_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        impact = order.update_status_bywin(window_id, order_update_dict)
        if impact == 1:
            return json_response(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(DB_ERROR, CODE_MESSAGE.get(DB_ERROR))
    else:
        return json_response(PARAM_REQUIRED, order_update_form.errors)


@exception_handled
@window_token_required
@post_required
def window_order_delete(request):
    delete_id_list_form = DeleteIdListForm(request.POST)
    if delete_id_list_form.is_valid():
        delete_id_list_dict = delete_id_list_form.cleaned_data
        delete_id_list = delete_id_list_dict['data']
        window_id = request.user_meta['window_model'].id
        order_id_list_fail_to_delete = order.delete_bywin(window_id, delete_id_list)
        return json_response_from_object(OK, order_id_list_fail_to_delete, 'orderIdList')
    else:
        return json_response(PARAM_REQUIRED, delete_id_list_form.errors)


@exception_handled
@window_token_required
@post_required
def window_comment_reply(request):
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply_dict = reply_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        order_model = order.get_order_byid_bywin(window_id, reply_dict)
        order_dish_model = orderdish.get_order_dish_byid(order_model, reply_dict)
        if order_dish_model.comment_time:  # user can only make reply on comments
            if order_dish_model.reply_time is None:
                orderdish.update_reply(order_dish_model, reply_dict)
                return json_response(OK, CODE_MESSAGE.get(OK))
            else:
                return json_response(ORDER_DISH_REPLIED, CODE_MESSAGE.get(ORDER_DISH_REPLIED))
        else:
            return json_response(ORDER_STATUS_ERROR, CODE_MESSAGE.get(ORDER_STATUS_ERROR))
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


@exception_handled
@window_token_required
@post_required
def window_sales_dish(request):
    sales_form = SalesForm(request.POST)
    if sales_form.is_valid():
        sales_dict = sales_form.cleaned_data
        # print sales_dict
        window_model = request.user_meta['window_model']
        result_dict = stat_window_sales(window_model, sales_dict)
        return json_response_from_object(OK, result_dict)
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


"""
    promotion_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': promotion_form})
"""