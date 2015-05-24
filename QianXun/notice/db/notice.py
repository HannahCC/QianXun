__author__ = 'Hannah'
from QianXun.notice.models import CanteenNotice, SchoolNotice
from utils.Pagination import get_paginator
from QianXun.notice.beans import NoticeBean, CanteenNoticeDetailBean, SchoolNoticeDetailBean


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


def find_school_notice_list_by_word(school_model, search_words):
    school_notice_list = SchoolNotice.objects.filter(school=school_model, title__icontains=search_words)
    school_notice_list_bean = [SchoolNoticeDetailBean(notice) for notice in school_notice_list]
    return school_notice_list_bean


def find_canteen_notice_list_by_word(canteen_model, seach_words):
    canteen_notice_list = CanteenNotice.objects.filter(canteen=canteen_model, title__icontains=seach_words)
    canteen_notice_list_bean = [CanteenNoticeDetailBean(notice) for notice in canteen_notice_list]
    return canteen_notice_list_bean