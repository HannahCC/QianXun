# -*- coding:utf-8 _*-
__author__ = 'Hannah'
from QianXun.orders.models import DeliverTime
from QianXun.orders.beans import DeliverTimeBean
from utils.Pagination import get_paginator


def get_deliver_time_bean_list_bywindow(window_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    deliver_time_list = DeliverTime.objects.filter(window_id__exact=window_id, is_valid=1).order_by('date', 'time')[paginator[0]:paginator[1]]
    deliver_time_bean_list = []
    for deliver_time in deliver_time_list:
        deliver_time_bean = DeliverTimeBean(deliver_time)
        deliver_time_bean_list.append(deliver_time_bean)
    return deliver_time_bean_list


def create(deliver_time, is_commit=True):
    if is_commit:
        deliver_time.save()
        new_deliver_time = DeliverTimeBean(deliver_time)
    else:
        new_deliver_time = deliver_time.save(commit=False)
    return new_deliver_time


def update(window_id, deliver_time_updated_dict):
    impact = DeliverTime.objects.filter(id__exact=deliver_time_updated_dict['deliver_time'],
                                        window_id__exact=window_id, is_valid=1).update(
        date=deliver_time_updated_dict['date'], time=deliver_time_updated_dict['time'])
    return impact


def delete(window_id, delete_id_list):
    impact = 0
    for deliver_time_id in delete_id_list:
        impact += DeliverTime.objects.filter(id__exact=deliver_time_id['id'], window_id__exact=window_id, is_valid=1)\
            .update(is_valid=0)
    return impact
