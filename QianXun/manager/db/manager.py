__author__ = 'Jeremy'

from QianXun.manager.models import SchoolManager, CanteenManager
from QianXun.notice.models import SchoolNotice, CanteenNotice
from QianXun.manager.beans import ManagerBean
from QianXun.notice.beans import SchoolNoticeDetailBean, CanteenNoticeDetailBean
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import get_serial_number
from datetime import datetime, date
from conf.enum_value import IS_VALID


def school_get_by_username(login_dict):
    manager = SchoolManager.objects.get(user_name__exact=login_dict["user_name"],
                                        password__exact=login_dict["password"], is_valid=IS_VALID[1][0])
    return manager


def canteen_get_by_username(login_dict):
    manager = CanteenManager.objects.get(user_name__exact=login_dict["user_name"],
                                        password__exact=login_dict["password"], is_valid=IS_VALID[1][0])
    return manager


def school_update_token(manager):
    manager.token = get_serial_number(manager.id)
    manager.save()
    manager_bean = ManagerBean(manager)
    return manager_bean

def canteen_update_token(manager):
    manager.token = get_serial_number(manager.id)
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
    manager_model.password = password_dict['password']
    manager_model.save()
    manager_bean = ManagerBean(manager_model)
    return manager_bean

def get_upper_notice(manager_model):
    canteen = manager_model.canteen
    notice_list = SchoolNotice.objects.filter(school_id__exact=canteen.school_id)
    return_bean_list = [SchoolNoticeDetailBean(notice) for notice in notice_list]
    return return_bean_list

def get_canteen_notice(manager_model):
    canteen = manager_model.canteen
    notice_list = CanteenNotice.objects.filter(canteen_id__exact=canteen.id)
    return_bean_list = [CanteenNoticeDetailBean(notice) for notice in notice_list]
    return return_bean_list
