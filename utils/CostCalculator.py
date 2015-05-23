# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from conf.default_value import VIP_DISCOUNT, DELIVERY_COST
import re


def get_deliver_cost():
    return DELIVERY_COST


def get_vip_discount(cost):
    new_cost = cost*VIP_DISCOUNT
    return new_cost


def get_promotions_discount(cost, promotion_list):
    """
    遍历该窗口参加的所有活动
    当前只有满减活动(活动ID为1)需要系统重新计算价格，由__process_manjian_discount()方法进行处理
    并且获取窗口的活动列表时，由于已经使用"-rules"排序，
    则活动 “满20减4”比“满10减2”会先遍历到，只要满足其中一个，则退出循环
    """
    for my_promotion in promotion_list:
        if my_promotion.pro_type.id == 1:
            new_cost = __process_manjian_discount(cost, my_promotion.rules)
            if new_cost != cost:
                break
        # if my_promotion.pro_type.id == 2:  # 可在此添加新的活动处理函数
    return new_cost


def __process_manjian_discount(cost, rules):
    m = re.search(ur"[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+(\d+)", rules)
    standard = int(m.group(1))
    discount = int(m.group(2))
    if cost >= standard:
        cost -= discount
    return cost