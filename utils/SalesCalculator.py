# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from QianXun.orders.db import order, orderdish
from datetime import datetime


def window_sales_calculate(window_model):
    """
    增量计算窗口，同时计算对应菜品的销量
    避免对窗口/菜品销量的并发操作,每次增加订单，并不会及时增加对应菜品的销量，而是在显示菜品的时候才计算对应的销量
    """
    # 得到该窗口上次计算之后 已完成的所有订单
    order_model_list = order.get_order_list_of_window(window_model)
    window_model.calculate_time = datetime.now()
    window_model.save()   # 更新数据库中窗口的销量的计算时间
    sales = window_model.sales
    for order_model in order_model_list:
        order_dish_model_list = orderdish.get_dish_list_byorder(order_model)
        for order_dish_model in order_dish_model_list:
            __dish_sales_calculate(order_dish_model.dish, order_dish_model)
            sales += order_dish_model.number  # 将订单中的菜品的份数累加到原销量上
    window_model.sales = sales
    window_model.save()   # 更新数据库中窗口的销量
    return window_model


def __dish_sales_calculate(dish_model, orderdish_model):
    """
    每次计算窗口的销量时，同时计算窗口下菜品的销量
    """
    dish_model.sales += orderdish_model.number
    dish_model.save()  # 更新数据库中菜品的销量、评级、评论数
    return dish_model

