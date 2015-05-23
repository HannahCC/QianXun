# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from QianXun.orders.db import orderdish
from datetime import datetime


def dish_grade_calculate(dish_model):
    """
    增量计算菜品，同时计算对应窗口的评级
    避免对窗口/菜品评级的并发操作,每次增加评价，并不会及时更改对应菜品的评级，而是在显示菜品的时候才计算对应的评级
    """
    # 得到该菜品上次计算之后 已完成的所有订单
    order_dish_model_list = orderdish.get_comment_list_bydish(dish_model)
    dish_model.calculate_time = datetime.now()
    dish_model.save()   # 更新数据库中窗口的销量的计算时间
    grade = dish_model.grade
    comment_number = dish_model.comment_number
    new_grade_sum = 0.0   # 新增评分的总和
    new_comment_number = 0   # 新增评论的数量
    for order_dish_model in order_dish_model_list:
        grade = (grade*comment_number + order_dish_model.grade)/(comment_number+1)
        comment_number += 1
        new_grade_sum += order_dish_model.grade
        new_comment_number += 1
    dish_model.grade = grade
    dish_model.comment_number = comment_number
    dish_model.save()   # 更新数据库中菜品的评级和评论数量
    __window_grade_calculate(dish_model.window, new_grade_sum, new_comment_number)  # 更新该菜品所在窗口的评级和评论数
    return dish_model


def __window_grade_calculate(window_model, new_grade_sum, new_comment_number):
    """
    每次计算菜品的评级时，同时计算所在窗口的评级
    需要考虑多个菜品同时改变窗口的评级
    """
    grade = window_model.grade
    comment_number = window_model.comment_number
    comment_number_sum = comment_number+new_comment_number
    grade = (grade * comment_number + new_grade_sum * new_comment_number)/comment_number_sum
    window_model.grade = grade
    window_model.comment_number = comment_number_sum
    window_model.save()  # 更新数据库中窗口的评级、评论数
    return window_model

