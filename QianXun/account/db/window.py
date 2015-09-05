__author__ = 'Hannah'
from QianXun.account.models import Window
from QianXun.account.beans import WindowBean
from datetime import datetime
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import new_token
from utils.SalesCalculator import window_sales_calculate
from utils.CostCalculator import get_promotion_str_from_list
from conf.enum_value import WINDOW_STATUS


# register
def isUnregistered(user_name):
    window_list = Window.objects.filter(user_name__exact=user_name)
    if len(window_list)==0:
        return True
    else:
        return False

def window_model_to_bean(window_model):
    window_model = window_sales_calculate(window_model)  # calculate sales of dish in the same window
    window_bean = WindowBean(window_model)
    return window_bean


def get_by_token(token):
    window_model = Window.objects.get(token__exact=token, is_valid=1)
    return window_model


def get_by_id(window_id):
    window_model = Window.objects.get(id__exact=window_id)
    window_bean = WindowBean(window_model)
    return window_bean


def get_by_username(window_login_dict):
    window_model = Window.objects.get(user_name__exact=window_login_dict['user_name'], is_valid=1)
    return window_model


def get_window_bean_list_bycanteen(canteen_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    window_model_list = Window.objects.filter(canteen__exact=canteen_id, is_valid=1, window_status=WINDOW_STATUS[3][0]).order_by('-sales')[paginator[0]: paginator[1]]
    window_bean_list = []
    for window_model in window_model_list:
        print 'here'
        window_bean = window_model_to_bean(window_model)
        window_bean_list.append(window_bean)
    return window_bean_list


def get_window_bean_list_byname(school_id, window_name, pagination_dict):
    paginator = get_paginator(pagination_dict)
    window_model_list = Window.objects.filter(school_id__exact=school_id, window_name__icontains=window_name,window_status=WINDOW_STATUS[3][0],
                                              is_valid=1).order_by('-sales')[paginator[0]: paginator[1]]
    window_bean_list = []
    for window_model in window_model_list:
        window_bean = window_model_to_bean(window_model)
        window_bean_list.append(window_bean)
    return window_bean_list


def get_window_bean_list_byid(window_id_list):
    window_bean_list = []
    for window_id in window_id_list:
        window_model = Window.objects.filter(id__exact=window_id['window_id'], is_valid=1)
        if len(window_model) == 1:
            window_bean = window_model_to_bean(window_model[0])
            window_bean_list.append(window_bean)
    return window_bean_list


def update_promotion_list(window_model):
    promotion_model_list = window_model.promotions_set.filter(is_valid__exact=1).order_by("pro_type", "-rules")
    promotion_str = get_promotion_str_from_list(promotion_model_list)
    window_model.promotion_list = promotion_str
    window_model.save()
    return window_model


def update_promotion_number(window_model, promotion_number_extra):
    window_model.promotion_number += promotion_number_extra
    window_model.save()
    return window_model


def update_dish_number(window_model, dish_number_extra):
    window_model.dish_number += dish_number_extra
    window_model.save()
    return window_model


def update_deliver_time_number(window_model, deliver_time_number_extra):
    window_model.deliver_time_number += deliver_time_number_extra
    window_model.save()
    return window_model


def delete(window_id):
    impact = Window.objects.filter(id__exact=window_id, is_valid=1).update(
        is_valid=0, update_time=datetime.now())
    return impact


def create(window, is_commit=True):
    if is_commit:
        window_model = window.save()
    else:
        window_model = window.save(commit=False)
    return window_model


def update_profile(window_model, window_profile_dict):
    window_model.name = window_profile_dict['name']
    window_model.window_name = window_profile_dict['window_name']
    window_model.window_status = window_profile_dict['window_status']
    window_model.save()
    return window_model


def update_profile_image(window_model, window_profile_dict):
    window_model.img_addr = window_profile_dict['img_addr']
    window_model.save()
    return window_model


def update_token(window_model, window_login_dict):
    window_model.registration_id = window_login_dict['registration_id']
    window_model.client_id = window_login_dict['client_id']
    window_model.version = window_login_dict['version']
    window_model.token = new_token()
    window_model.save()
    return window_model_to_bean(window_model)


def update_password(window_model, window_password_dict):
    window_model.password = window_password_dict['new_password']
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


def update_status(window_verify_dict):
    window_id = window_verify_dict['window_id']
    window_status = window_verify_dict['window_status']
    window_model = Window.objects.get(id__exact=window_id)
    window_model.window_status = window_status
    window_model.save()
    return window_model


def delete_all():
    impact = Window.objects.all().delete()
    return impact