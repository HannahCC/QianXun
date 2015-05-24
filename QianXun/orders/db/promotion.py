# -*- coding:utf-8 _*-
__author__ = 'Hannah'
from QianXun.orders.models import Promotions
from QianXun.orders.beans import PromotionBean
from utils.Pagination import get_paginator


def get_window_id_list_byprotype(school_id, pro_type_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    window_id_list = Promotions.objects.values('window_id').distinct()\
        .filter(pro_type_id__exact=pro_type_id, window__school_id__exact=school_id,
                is_valid=1)[paginator[0]: paginator[1]]
    return window_id_list


def get_promotion_list_bywindow(window_id, pagination_dict, order_by='-rules'):
    paginator = get_paginator(pagination_dict)
    promotion_list = Promotions.objects.filter(window__exact=window_id, is_valid=1).order_by(order_by)[paginator[0]: paginator[1]]
    return promotion_list


def get_promotion_bean_list_bywindow(window_id, pagination_dict, order_by='-rules'):
    paginator = get_paginator(pagination_dict)
    promotion_list = Promotions.objects.filter(window__exact=window_id, is_valid=1).order_by('pro_type_id', order_by)[paginator[0]: paginator[1]]
    promotion_bean_list = []
    for promotion_model in promotion_list:
        promotion_bean = PromotionBean(promotion_model)
        promotion_bean_list.append(promotion_bean)
    return promotion_bean_list


def create(promotion, is_commit=True):
    if is_commit:
        promotion.save()
        new_promotion = PromotionBean(promotion)
    else:
        new_promotion = promotion.save(commit=False)
    return new_promotion


def update(window_id, promotion_update_dict):
    impact = Promotions.objects.filter(id__exact=promotion_update_dict['promotion'], window_id__exact=window_id, is_valid=1)\
        .update(pro_type=promotion_update_dict['pro_type'], rules=promotion_update_dict['rules'])
    return impact


def delete(window_id, promotion_id_list):
    impact = 0
    for promotion_id in promotion_id_list:
        impact += Promotions.objects.filter(id__exact=promotion_id['promotion'], window_id__exact=window_id, is_valid=1)\
            .update(is_valid=0)
    return impact
