__author__ = 'Hannah'
from QianXun.notice.models import CanteenNotice
from utils.Pagination import get_paginator
from QianXun.notice.beans import NoticeBean, CanteenNoticeDetailBean


def get_canteen_notice_bean_list_bycanteen(canteen_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    canteen_notice_model_list = CanteenNotice.objects.filter(canteen=canteen_model).order_by('-update_time')[paginator[0]:paginator[1]]
    canteen_notice_bean_list = []
    for canteen_notice_model in canteen_notice_model_list:
        canteen_notice_bean = NoticeBean(canteen_notice_model)
        canteen_notice_bean_list.append(canteen_notice_bean)
    return canteen_notice_bean_list


def get_canteen_notice_detail_bean_byid(canteen_model, notice_detail_display_form):
    canteen_notice_model = CanteenNotice.objects.get(canteen=canteen_model, id=notice_detail_display_form['notice'])
    canteen_notice_detail_bean = CanteenNoticeDetailBean(canteen_notice_model)
    return canteen_notice_detail_bean