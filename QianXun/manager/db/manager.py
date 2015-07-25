# -*- encoding=utf-8 -*-
__author__ = 'Jeremy'

from QianXun.manager.models import SchoolManager, CanteenManager
from QianXun.account.models import Window
from QianXun.account.beans import WindowBean
from QianXun.notice.models import SchoolNotice, CanteenNotice
from QianXun.manager.beans import ManagerBean
from QianXun.notice.beans import SchoolNoticeDetailBean, CanteenNoticeDetailBean
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import new_token
from conf.enum_value import IS_VALID


def delete_token(manager_model):
    manager_model.token = ''
    manager_model.save()
    return manager_model


def school_get_by_username(login_dict):
    manager = SchoolManager.objects.get(user_name__exact=login_dict["user_name"],is_valid=IS_VALID[1][0])
    return manager


def canteen_get_by_username(login_dict):
    manager = CanteenManager.objects.get(user_name__exact=login_dict["user_name"],is_valid=IS_VALID[1][0])
    return manager


def school_update_token(manager):
    manager.token = new_token()
    manager.save()
    manager_bean = ManagerBean(manager)
    return manager_bean


def canteen_update_token(manager):
    manager.token = new_token()
    manager.save()
    manager_bean = ManagerBean(manager)
    return manager_bean


def school_get_by_token(token):
    manager = SchoolManager.objects.get(token__exact=token, is_valid=IS_VALID[1][0])
    return manager


def canteen_get_by_token(token):
    manager = CanteenManager.objects.get(token__exact=token, is_valid=IS_VALID[1][0])
    return manager


def update_password(manager_model, password_dict):
    manager_model.password = password_dict['new_password']
    manager_model.save()
    manager_bean = ManagerBean(manager_model)
    return manager_bean

def get_upper_notice(manager_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    canteen = manager_model.canteen
    notice_list = SchoolNotice.objects.filter(school_id__exact=canteen.school_id,is_valid=1).order_by('-update_time')[paginator[0]:paginator[1]]
    return_bean_list = [SchoolNoticeDetailBean(notice) for notice in notice_list]
    return return_bean_list


def get_upper_notice_number(manager_model):
    canteen = manager_model.canteen
    notice_list = SchoolNotice.objects.filter(school_id__exact=canteen.school_id,is_valid=1)
    return len(notice_list)


def get_all_school_notice(manager_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    school = manager_model.school
    notice_list = SchoolNotice.objects.filter(school_id__exact=school.id,is_valid=1).order_by('-update_time')[paginator[0]:paginator[1]]
    return [SchoolNoticeDetailBean(notice) for notice in notice_list]


def get_all_school_notice_number(manager_model):
    school = manager_model.school
    notice_list = SchoolNotice.objects.filter(school_id__exact=school.id,is_valid=1)
    return len(notice_list)


def get_canteen_notice(manager_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    canteen = manager_model.canteen
    notice_list = CanteenNotice.objects.filter(canteen_id__exact=canteen.id,is_valid=1).order_by('-update_time')[paginator[0]:paginator[1]]
    return_bean_list = [CanteenNoticeDetailBean(notice) for notice in notice_list]
    return return_bean_list


def get_canteen_notice_number(manager_model):
    canteen = manager_model.canteen
    notice_list = CanteenNotice.objects.filter(canteen_id__exact=canteen.id,is_valid=1)
    return len(notice_list)


def get_school_windows(manager_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    school = manager_model.school
    windows_list = Window.objects.filter(school_id__exact=school.id,is_valid=1).order_by('canteen','-sales')[paginator[0]:paginator[1]]
    return_bean_list = [WindowBean(window) for window in windows_list]
    return return_bean_list


def get_school_windows_number(manager_model):
    school = manager_model.school
    windows_list = Window.objects.filter(school_id__exact=school.id,is_valid=1)
    return len(windows_list)
    

def get_canteen_windows(manager_model, pagination_dict):
    # 一个餐厅管理员只能管理一个餐厅
    paginator = get_paginator(pagination_dict)
    order_by = pagination_dict['order_by']
    if not order_by:
        order_by = '-sales'
    windows_list = Window.objects.filter(canteen_id__exact=manager_model.canteen.id,is_valid=1).order_by(order_by)[paginator[0]:paginator[1]]
    return_bean_list = [WindowBean(window) for window in windows_list]
    return return_bean_list


def get_canteen_windows_number(manager_model):
    canteen = manager_model.canteen
    windows_list = Window.objects.filter(canteen_id__exact=canteen.id,is_valid=1)
    return len(windows_list)


def search_school_windows_by_name(school_model, search_words):
    window_list = Window.objects.filter(school_id__exact=school_model.id, is_valid=1, window_name__contains=search_words).order_by('canteen','-sales')
    return [WindowBean(window) for window in window_list]


def search_canteen_windows_by_name(canteen_model, search_words):
    window_list = Window.objects.filter(canteen_id__exact=canteen_model.id, is_valid=1, window_name__contains=search_words).order_by('-sales')
    return [WindowBean(window) for window in window_list]
