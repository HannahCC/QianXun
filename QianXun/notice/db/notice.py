__author__ = 'Hannah'
from QianXun.notice.models import CanteenNotice, SchoolNotice
from utils.Pagination import get_paginator
from QianXun.notice.beans import CanteenNoticeDetailBean, SchoolNoticeDetailBean


def get_canteen_notice_bean_list_bycanteen(canteen_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    canteen_notice_model_list = CanteenNotice.objects.filter(canteen=canteen_model,is_valid=1).order_by('-update_time')[paginator[0]:paginator[1]]
    canteen_notice_bean_list = []
    for canteen_notice_model in canteen_notice_model_list:
        canteen_notice_bean = CanteenNoticeDetailBean(canteen_notice_model)
        canteen_notice_bean_list.append(canteen_notice_bean)
    return canteen_notice_bean_list


def get_canteen_notice_detail_bean_byid(canteen_model, notice_detail_display_form):
    canteen_notice_model = CanteenNotice.objects.get(canteen=canteen_model, id=notice_detail_display_form['notice'],is_valid=1)
    canteen_notice_detail_bean = CanteenNoticeDetailBean(canteen_notice_model)
    return canteen_notice_detail_bean


def find_school_notice_list_by_word(school_model, search_words):
    school_notice_list = SchoolNotice.objects.filter(school=school_model, title__icontains=search_words,is_valid=1).order_by('-update_time')
    school_notice_list_bean = [SchoolNoticeDetailBean(notice) for notice in school_notice_list]
    return school_notice_list_bean


def find_canteen_notice_list_by_word(canteen_model, seach_words):
    canteen_notice_list = CanteenNotice.objects.filter(canteen=canteen_model, title__icontains=seach_words,is_valid=1).order_by('-update_time')
    canteen_notice_list_bean = [CanteenNoticeDetailBean(notice) for notice in canteen_notice_list]
    return canteen_notice_list_bean

def find_canteen_notice_list_by_canteen_manager(canteen_manager_model):
    canteen_notice_list = CanteenNotice.objects.filter(manager=canteen_manager_model,is_valid=1).order_by('-update_time')
    canteen_notice_list_bean = [CanteenNoticeDetailBean(notice) for notice in canteen_notice_list]
    return canteen_notice_list_bean


def find_school_notice_list_by_school_manager(school_manager_model):
    school_notice_list = SchoolNotice.objects.filter(manager=school_manager_model,is_valid=1).order_by('-update_time')
    school_notice_list_bean = [SchoolNoticeDetailBean(notice) for notice in school_notice_list]
    return school_notice_list_bean

def get_canteen_notice_by_id(canteen_notice_id):
    canteen_notice = CanteenNotice.objects.get(id__exact=canteen_notice_id,is_valid=1)
    return canteen_notice


def get_school_notice_by_id(canteen_notice_id):
    canteen_notice = SchoolNotice.objects.get(id__exact=canteen_notice_id,is_valid=1)
    return canteen_notice


def cm_modify_notice(already_notice,modify_form_dict):
    # canteen_notice_model = CanteenNotice.objects.get(id__exact=modify_form_dict["id"])
    already_notice.title = modify_form_dict["title"]
    already_notice.content = modify_form_dict["content"]
    already_notice.save()
    canteen_notice_bean = CanteenNoticeDetailBean(already_notice)
    return canteen_notice_bean


def cm_create_notice(manager, create_form_dict):
    notice_model = CanteenNotice()
    notice_model.manager = manager
    notice_model.canteen = manager.canteen
    notice_model.title = create_form_dict["title"]
    notice_model.content = create_form_dict["content"]
    notice_model.save()
    return CanteenNoticeDetailBean(notice_model)


def delte_notice(notice_model):
    notice_model.is_valid = 0
    notice_model.save()
    return True



def sm_modify_notice(already_notice,modify_form_dict):
    # canteen_notice_model = CanteenNotice.objects.get(id__exact=modify_form_dict["id"])
    already_notice.title = modify_form_dict["title"]
    already_notice.content = modify_form_dict["content"]
    already_notice.save()
    canteen_notice_bean = SchoolNoticeDetailBean(already_notice)
    return canteen_notice_bean


def sm_create_notice(manager, create_form_dict):
    notice_model = SchoolNotice()
    notice_model.manager = manager
    notice_model.school = manager.school
    notice_model.title = create_form_dict["title"]
    notice_model.content = create_form_dict["content"]
    notice_model.save()
    return SchoolNoticeDetailBean(notice_model)