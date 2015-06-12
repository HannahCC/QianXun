from django.shortcuts import render_to_response

from utils.Decorator import window_token_required, post_required, exception_handled
from utils.Serializer import json_response, json_response_from_object, json_back
from conf.resp_code import *
from conf.default_value import PROMOTION_MAX, DELIVER_TIME_MAX, DISH_MAX
from conf.enum_value import ORDER_STATUS
from forms import PaginationForm, PromotionForm, PromotionUpdateForm, DeliverTimeForm, DeliverTimeUpdateForm, DishForm, DishUpdateForm, \
    OrderDetailDisplayForm, WindowOrderUpdateForm, ReplyForm, SalesForm
from QianXun.orders.db import promotion, deliver_time, dish, order, orderdish
from QianXun.orders.beans import DishSaleBean
from QianXun.account.db import window
import operator

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
    promotion_id_list_str = request.POST.get('data', "")
    if promotion_id_list_str.startswith("[{") and promotion_id_list_str.endswith("}]"):
        window_model = request.user_meta['window_model']
        promotion_id_list = json_back(promotion_id_list_str)
        promotion.delete(window_model.id, promotion_id_list)
        window.update_promotion_list(window_model)
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


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
    deliver_time_id_list_str = request.POST.get('data', "")
    if deliver_time_id_list_str.startswith("[{") and deliver_time_id_list_str.endswith("}]"):
        deliver_time_id_list = json_back(deliver_time_id_list_str)
        window_id = request.user_meta['window_model'].id
        deliver_time.delete(window_id, deliver_time_id_list)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


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
def window_dish_delete(request):
    dish_id_list_str = request.POST.get('data', "")
    if dish_id_list_str.startswith("[{") and dish_id_list_str.endswith("}]"):
        dish_id_list = json_back(dish_id_list_str)
        window_id = request.user_meta['window_model'].id
        dish.delete(window_id, dish_id_list)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


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
    order_id_list_str = request.POST.get('data', "")
    if order_id_list_str.startswith("[{") and order_id_list_str.endswith("}]"):
        order_id_list = json_back(order_id_list_str)
        window_id = request.user_meta['window_model'].id
        order_id_list_fail_to_delete = order.delete_bywin(window_id, order_id_list)
        return json_response_from_object(OK, order_id_list_fail_to_delete, 'orderIdList')
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


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
    sales_dish_form = SalesForm(request.POST)
    if sales_dish_form.is_valid():
        sales_dish_dict = sales_dish_form.cleaned_data
        window_model = request.user_meta['window_model']
        # get all dishes of this window
        dish_model_list = dish.get_dish_list_bywin(window_model.id, {'page': 1, 'count': DISH_MAX})
        # get all orders of this window during given time interval, and calculate sales of dishes.
        sales_volume = 0
        dish_sale_dict = {}
        for dish_model in dish_model_list:
            dish_sale_dict.update({dish_model: 0})
        page = 1
        while True:
            order_model_list = order.get_order_list_ofwin(window_model, {'page': page, 'count': 1000}, sales_dish_dict)
            for order_model in order_model_list:
                sales_volume += order_model.food_cost
                order_dish_model_list = orderdish.get_dish_list_byorder(order_model)
                for order_dish_model in order_dish_model_list:
                    dish_model = order_dish_model.dish
                    dish_sale_dict.update({dish_model: dish_sale_dict.get(dish_model)+order_dish_model.number})
            page += 1
            if len(order_model_list) < 1000:
                break
        # make it serialized
        dish_sale_bean_list = []
        for dish_model, sale in dish_sale_dict.items():
            dish_sale_bean = DishSaleBean(dish_model, sale)
            dish_sale_bean_list.append(dish_sale_bean)
        # sorted by sales
        sorted_dish_sale_bean_list = sorted(dish_sale_bean_list, key=operator.attrgetter("sales"), reverse=True)
        result_dict = {"total": sales_volume, "dishList": sorted_dish_sale_bean_list}
        return json_response_from_object(OK, result_dict)
    else:
        return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))


"""
    promotion_form = PromotionForm()
    if request.method == 'GET':
        return render_to_response('test/testOrder.html', {'form': promotion_form})
"""