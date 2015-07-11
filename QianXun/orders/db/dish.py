__author__ = 'Hannah'
from QianXun.orders.models import Dish
from QianXun.orders.beans import DishBean
from utils.Pagination import get_paginator
from utils.SalesCalculator import window_sales_calculate
from utils.GradeCalculator import dish_grade_calculate


def dish_model_to_bean(dish_model):
    dish_grade_calculate(dish_model)  # calculate grade of dish
    window_sales_calculate(dish_model.window)  # calculate sales of dish in the same window
    dish_model = Dish.objects.get(id__exact=dish_model.id, is_valid=1)
    dish_bean = DishBean(dish_model)
    return dish_bean


# used by create order
def get_dish_list_cost(particular_dish_model_list):
    cost = 0.0
    for particular_dish_model in particular_dish_model_list:
        cost += particular_dish_model.price * particular_dish_model.number
    return cost


def get_dish_list_bywin(window_id, pagination_dict, order_by='sales'):
    paginator = get_paginator(pagination_dict)
    dish_model_list = Dish.objects.filter(window_id__exact=window_id, is_valid=1).order_by(order_by)[paginator[0]:paginator[1]]
    return dish_model_list


def get_dish_bean_list_bywin(window_id, pagination_dict, order_by='sales'):
    paginator = get_paginator(pagination_dict)
    dish_model_list = Dish.objects.filter(window_id__exact=window_id, is_valid=1).order_by(order_by)[paginator[0]:paginator[1]]
    dish_bean_list = []
    for dish_model in dish_model_list:
        dish_bean = DishBean(dish_model)
        dish_bean_list.append(dish_bean)
    return dish_bean_list


def get_dish_bean_list_byname(school_id, dish_name, pagination_dict, order_by='sales'):
    paginator = get_paginator(pagination_dict)
    dish_model_list = Dish.objects.filter(window__school_id__exact=school_id, dish_name__icontains=dish_name,
                                          is_valid=1).order_by(order_by)[paginator[0]:paginator[1]]
    dish_bean_list = []
    for dish_model in dish_model_list:
        dish_bean = DishBean(dish_model)
        dish_bean_list.append(dish_bean)
    return dish_bean_list


def create(dish_model, is_commit=True):
    if is_commit:
        dish_model.save()
        new_dish_model = DishBean(dish_model)
    else:
        new_dish_model = dish_model.save(commit=False)
    return new_dish_model


def update(window_id, dish_update_dict):
    impact = Dish.objects.filter(id__exact=dish_update_dict['dish'], window_id__exact=window_id, is_valid=1).update(
        dish_name=dish_update_dict['dish_name'], description=dish_update_dict['description'],
        is_heat=dish_update_dict['is_heat'], price=dish_update_dict['price'], img_addr=dish_update_dict['img_addr'])
    return impact


def delete(window_id, delete_id_list):
    impact = 0
    for dish_id in delete_id_list:
        impact += Dish.objects.filter(id__exact=dish_id['id'], window_id__exact=window_id, is_valid=1)\
            .update(is_valid=0)
    return impact


