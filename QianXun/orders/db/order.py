__author__ = 'Hannah'

from QianXun.orders.models import Orders
from QianXun.orders.beans import OrderBean, OrderDetailBean
from QianXun.orders.db import orderdish
from utils.Pagination import get_paginator
from datetime import datetime
from conf.enum_value import ORDER_STATUS


def create_bycus(order_dict):
    my_order = Orders()
    my_order.window = order_dict['window']
    my_order.customer = order_dict['customer']
    my_order.order_id = order_dict['order_id']
    my_order.promotion_list = order_dict['promotion_list']
    my_order.discount = order_dict['discount']
    my_order.food_cost = order_dict['food_cost']
    my_order.deliver_cost = order_dict['deliver_cost']

    my_order.building = order_dict['building']
    my_order.address = order_dict['address']
    my_order.notes = order_dict['notes']
    my_order.deliver_time = order_dict['deliver_time']
    my_order.save()
    return my_order


def get_order_byid_bycus(customer_id, order_dict):
    my_order = Orders.objects.get(customer_id__exact=customer_id, id__exact=order_dict['order'], is_valid2customer=1)
    return my_order


def get_order_byid_bywin(window_id, order_dict):
    my_order = Orders.objects.get(window_id__exact=window_id, id__exact=order_dict['order'], is_valid2window=1)
    return my_order


def get_order_bean_list_bycus(customer_id, order_status, pagination_dict):
    paginator = get_paginator(pagination_dict)
    if order_status == '':
        order_list = Orders.objects.filter(customer_id__exact=customer_id, is_valid2customer=1).order_by('-update_time')[paginator[0]:paginator[1]]
    else:
        order_list = Orders.objects.filter(customer_id__exact=customer_id, order_status=order_status, is_valid2customer=1).order_by('-update_time')[paginator[0]:paginator[1]]
    order_bean_list = []
    for my_order in order_list:
        order_dish_bean_list = orderdish.get_dish_bean_list_byorder(my_order)
        order_bean = OrderBean(my_order, order_dish_bean_list)
        order_bean_list.append(order_bean)
    return order_bean_list


def get_order_bean_list_bywin(window_id, order_status, pagination_dict):
    paginator = get_paginator(pagination_dict)
    if order_status:
        order_list = Orders.objects.filter(window_id__exact=window_id, order_status=order_status,
                                           is_valid2window=1).order_by('-update_time')[paginator[0]:paginator[1]]
    else:
        order_list = Orders.objects.filter(window_id__exact=window_id, order_status__gt=ORDER_STATUS[0][0],
                                           is_valid2window=1).order_by('-update_time')[paginator[0]:paginator[1]]
    order_bean_list = []
    for my_order in order_list:
        order_dish_bean_list = orderdish.get_dish_bean_list_byorder(my_order)
        order_bean = OrderBean(my_order, order_dish_bean_list)
        order_bean_list.append(order_bean)
    return order_bean_list


def get_order_detail_byid_bycus(customer_id, order_detail_display_dict):
    my_order = Orders.objects.get(customer_id__exact=customer_id, id__exact=order_detail_display_dict['order'], is_valid2customer=1)
    order_dish_bean_list = orderdish.get_dish_bean_list_byorder(my_order)
    order_detail_bean = OrderDetailBean(my_order, order_dish_bean_list)
    return order_detail_bean


def get_order_detail_byid_bywin(window_id, order_detail_display_dict):
    my_order = Orders.objects.get(window_id__exact=window_id, id__exact=order_detail_display_dict['order'], is_valid2window=1)
    order_dish_bean_list = orderdish.get_dish_bean_list_byorder(my_order)
    order_detail_bean = OrderDetailBean(my_order, order_dish_bean_list)
    return order_detail_bean


# order_status validation has done in FORM
# use old_order_status to make concurrency control
def update_status_bycus(customer_id, order_update_dict):
    new_order_status = order_update_dict['new_order_status']
    if new_order_status == ORDER_STATUS[1][0]:  # pay
        impact = Orders.objects.filter(customer_id__exact=customer_id, id__exact=order_update_dict['order'],
                                       order_status=order_update_dict['old_order_status'], is_valid2customer=1). \
            update(order_status=new_order_status, deal_time=datetime.now(), update_time=datetime.now())
    else:
        impact = Orders.objects.filter(customer_id__exact=customer_id, id__exact=order_update_dict['order'],
                                       order_status=order_update_dict['old_order_status'], is_valid2customer=1). \
            update(order_status=new_order_status, update_time=datetime.now())
    return impact


# order_status validation has done in FORM
# use old_order_status to make concurrency control
def update_status_bywin(window_id, order_update_dict):
    impact = Orders.objects.filter(window_id__exact=window_id, id__exact=order_update_dict['order'],
                                   order_status=order_update_dict['old_order_status'], is_valid2window=1). \
        update(order_status=order_update_dict['new_order_status'], update_time=datetime.now())
    return impact


def delete_bycus(customer_id, delete_id_list):
    order_id_list_fail_to_delete = []
    for order_id in delete_id_list:
        my_order_list = Orders.objects.filter(customer_id__exact=customer_id, id__exact=order_id['id'], is_valid2customer=1)
        if my_order_list and len(my_order_list) == 1:
            my_order = my_order_list[0]
            order_status = my_order.order_status
            # only order in un_pay status or complete status can be deleted
            if order_status == ORDER_STATUS[0][0] or order_status % 10 == 0:
                my_order.is_valid2customer = 0
                my_order.save()
            else:
                order_id_list_fail_to_delete.append(order_id['id'])
        else:
            order_id_list_fail_to_delete.append(order_id['id'])
    return order_id_list_fail_to_delete


def delete_bywin(window_id, delete_id_list):
    order_id_list_fail_to_delete = []
    for order_id in delete_id_list:
        my_order_list = Orders.objects.filter(window_id__exact=window_id, id__exact=order_id['id'], is_valid2window=1)
        if my_order_list and len(my_order_list) == 1:
            my_order = my_order_list[0]
            order_status = my_order.order_status
            # only order in complete status can be deleted
            if order_status % 10 == 0:
                my_order.is_valid2window = 0
                my_order.save()
            else:
                order_id_list_fail_to_delete.append(order_id['id'])
        else:
            order_id_list_fail_to_delete.append(order_id['id'])
    return order_id_list_fail_to_delete


# used when calculate sales
def get_order_list_of_window(window_model):
    order_model_list = window_model.orders_set.filter(order_status__exact=ORDER_STATUS[7][0],
                                                      update_time__gte=window_model.calculate_time)
    return order_model_list


# used when calculate window-dish sales
def get_order_list_ofwin(window_model, pagination_dict, sales_dish_dict):
    paginator = get_paginator(pagination_dict)
    date_from = sales_dish_dict['start_date']
    date_to = sales_dish_dict['end_date']
    order_model_list = window_model.orders_set.filter(order_status__exact=ORDER_STATUS[7][0],
                                                      update_time__range=(date_from, date_to))[paginator[0]:paginator[1]]
    return order_model_list