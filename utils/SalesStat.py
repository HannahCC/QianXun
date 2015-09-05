# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from QianXun.orders.db import dish, order, orderdish
from QianXun.orders.beans import DishSaleBean
from conf.default_value import  DISH_MAX
from conf.enum_value import IS_VALID
import operator


def stat_window_sales(window_model, sales_dict):
    """
    对给定窗口统计其在给定时间内菜品的销售量及窗口总销售额
    """
    # get all dishes of this window
    dish_model_list = dish.get_dish_list_bywin(window_model.id, {'page': 1, 'count': DISH_MAX})
    # get all orders of this window during given time interval, and calculate sales of dishes.
    sales_volume = 0
    dish_sale_dict = {}
    for dish_model in dish_model_list:
        dish_sale_dict.update({dish_model: 0})
    page = 1
    while True:
        order_model_list = order.get_order_list_ofwin(window_model, {'page': page, 'count': 1000}, sales_dict)
        for order_model in order_model_list:
            sales_volume += order_model.food_cost
            order_dish_model_list = orderdish.get_dish_list_byorder(order_model)
            for order_dish_model in order_dish_model_list:
                dish_model = order_dish_model.dish
                volume = dish_sale_dict.get(dish_model)
                dish_sale_dict.update({dish_model: volume+order_dish_model.number})
        page += 1
        if len(order_model_list) < 1000:
            break
    # make it serialized
    dish_sale_bean_list = []
    for dish_model, sale in dish_sale_dict.items():
        if dish_model.is_valid==IS_VALID[0][0] and sale==0:
            continue;
        dish_sale_bean = DishSaleBean(dish_model, sale)
        dish_sale_bean_list.append(dish_sale_bean)
    # sorted by sales
    sorted_dish_sale_bean_list = sorted(dish_sale_bean_list, key=operator.attrgetter("sales"), reverse=True)
    result_dict = {"total": sales_volume, "dishList": sorted_dish_sale_bean_list}
    return result_dict