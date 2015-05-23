__author__ = 'Hannah'
from QianXun.account.models import Window
from QianXun.account.beans import WindowBean
from datetime import datetime
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import get_serial_number
from utils.SalesCalculator import window_sales_calculate


def window_model_to_bean(window_model):
    window_model = window_sales_calculate(window_model)  # calculate sales of dish in the same window
    window_bean = WindowBean(window_model)
    return window_bean


def get_by_token(token):
    window_model = Window.objects.get(token__exact=token, is_valid=1)
    return window_model


def get_by_username(window_login_dict):
    window_model = Window.objects.get(user_name__exact=window_login_dict['user_name'], password__exact=window_login_dict['password'], is_valid=1)
    return window_model


def get_window_list(canteen_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    window_model_list = Window.objects.filter(canteen__exact=canteen_id, is_valid=1).order_by('window_name')[paginator[0]: paginator[1]]
    return window_model_list


def update_username(window_id, user_name):
    impact = Window.objects.filter(id__exact=window_id, is_valid=1).update(
        user_name=user_name, update_time=datetime.now())
    return impact


def update_password(window_id, password):
    impact = Window.objects.filter(id__exact=window_id, is_valid=1).update(
        password=password, update_time=datetime.now())
    return impact


def update_promotion_number(window_model, promotion_number_extra):
    window_model.promotion_number += promotion_number_extra
    window_model.save()
    return window_model


def delete(window_id):
    impact = Window.objects.filter(id__exact=window_id, is_valid=1).update(
        is_valid=0, update_time=datetime.now())
    return impact


def create(window):
    window_model = window.save()
    return window_model


def update_profile(window_model, window_profile_dict):
    window_model.name = window_profile_dict['name']
    window_model.img_addr = window_profile_dict['img_addr']
    window_model.window_name = window_profile_dict['window_name']
    window_model.window_status = window_profile_dict['window_status']
    window_model.canteen = window_profile_dict['canteen']
    window_model.save()
    return window_model


def update_token(window_model ,window_login_dict):
    window_model.client_id = window_login_dict['client_id']
    window_model.version = window_login_dict['version']
    window_model.token = get_serial_number(window_model.id)
    window_model.save()
    return window_model_to_bean(window_model)


def update_password(window_model, window_password_dict):
    window_model.password = window_password_dict['password']
    window_model.save()
    return window_model


def update_username(window_model, window_username_dict):
    window_model.user_name = window_username_dict['user_name']
    window_model.save()
    return window_model


def delete_token(window_model):
    window_model.token = ''
    window_model.save()
    return window_model