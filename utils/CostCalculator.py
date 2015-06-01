# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from conf.default_value import VIP_DISCOUNT, DELIVERY_COST
import re


def get_deliver_cost():
    return DELIVERY_COST


def get_vip_discount(cost):
    new_cost = cost*VIP_DISCOUNT
    return new_cost


def get_promotions_dict(cost, promotion_queryset):
    """
    算法：
    首先将活动按照活动需达到的金额标准对活动列表降序排列，没有金额标准的活动类别的活动排在序列结尾
    则活动 “满20减4”比“满10减2”会先遍历到，
    若cost = 25, old_standard_x将记录最先达到的活动标准，如遍历过“满20减4”后，old_standard_x = 20，
    再次检查下一则活动时，要求该活动的标准要达到此前已经达到的活动标准20，以此过滤掉“满10减2”这一类活动
    ps：同一类活动可以有多个活动被满足。如满10赠纸巾，满10赠饮料可以同时被参加。
    """
    promotion_list = __process_queryset2list(promotion_queryset)
    promotion_list.sort(cmp=__promotion_list_sorted_by_rule)
    old_standard_1 = -1
    old_standard_2 = -1
    promotion_list_1 = []
    promotion_list_2 = []
    promotion_list_3 = []

    for my_promotion in promotion_list:
        if my_promotion.pro_type.id == 1:
            new_standard_1 = __process_is_order_meet(cost, old_standard_1, my_promotion.rules)
            if new_standard_1 != -1:
                old_standard_1 = new_standard_1
                promotion_list_1.append(my_promotion.rules)
        if my_promotion.pro_type.id == 2:
            new_standard_2 = __process_is_order_meet(cost, old_standard_2, my_promotion.rules)
            if new_standard_2 != -1:
                old_standard_2 = new_standard_2
                promotion_list_2.append(my_promotion.rules)
        if my_promotion.pro_type.id == 3:
            promotion_list_3.append(my_promotion.rules)
        # if my_promotion.pro_type.id == 4:   # 可在此添加新的活动标准处理函数

    promotions_dict = {}
    promotions_dict.update({1: promotion_list_1})
    promotions_dict.update({2: promotion_list_2})
    promotions_dict.update({3: promotion_list_3})
    return promotions_dict


def __process_queryset2list(promotion_queryset):
    promotion_list = []
    for items in promotion_queryset:
        promotion_list.append(items)
    return promotion_list


def __promotion_list_sorted_by_rule(x, y):
    m = re.search(ur"[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+", x.rules)
    standard_x = 0
    if m:
        standard_x = int(m.group(1))
    m = re.search(ur"[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+", y.rules)
    standard_y = 0
    if m:
        standard_y = int(m.group(1))
    return standard_y - standard_x


def __process_is_order_meet(cost, old_standard, rules):
    m = re.search(ur"[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+\d*", rules)
    standard = float(m.group(1))
    if cost >= standard >= old_standard:
        return standard
    return -1


def get_promotion_str(promotions_dict):
    promotion_str = ""
    for (protype, rules) in promotions_dict.items():
        for rule in rules:
            promotion_str = ",".join([promotion_str, rule])
    promotion_str = promotion_str[1:len(promotion_str)]
    return promotion_str


def get_promotions_discount(cost, promotions_dict):
    """
    遍历该窗口参加的所有活动
    当前只有满减活动(活动ID为1)需要系统重新计算价格，由__process_manjian_discount()方法进行处理
    """
    for (protype, rules) in promotions_dict.items():
        if protype == 1:
            for rule in rules:
                cost = __process_manjian_discount(cost, rule)
        # if protype == 2:  # 可在此添加新的活动处理函数
    return cost


def __process_manjian_discount(cost, rules):
    m = re.search(ur"[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+(\d+)", rules)
    standard = int(m.group(1))
    discount = int(m.group(2))
    if cost >= standard:
        cost -= discount
    return cost