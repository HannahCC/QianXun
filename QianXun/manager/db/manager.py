__author__ = 'Jeremy'

from QianXun.manager.models import SchoolManager, CanteenManager
from QianXun.manager.beans import ManagerBean
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import get_serial_number
from datetime import datetime, date
from conf.enum_value import IS_VALID


def get_by_username(login_dict):
    manager = SchoolManager.objects.get(user_name__exact=login_dict["user_name"],
                                        password__exact=login_dict["password"], is_valid=IS_VALID[1][0])

    return manager


def update_token(manager):

    manager.token = get_serial_number(manager.id)
    manager.save()
    customer_bean = ManagerBean(manager)
    return customer_bean


def get_by_token(token):
    manager = SchoolManager.filter()
