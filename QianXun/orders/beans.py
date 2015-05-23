__author__ = 'Hannah'
from utils.TimeLocalize import convert_to_localtime, datetime_format, time_format
from datetime import time


class PromotionBean:
    def __init__(self, promotion_model):
        self.promotion_id = promotion_model.id
        self.pro_type_id = promotion_model.pro_type.id
        self.rules = promotion_model.rules


class DeliverTimeBean:
    def __init__(self, deliver_time_model):
        self.deliver_time_id = deliver_time_model.id
        self.date = deliver_time_model.date
        self.time = deliver_time_model.show_time()
        if isinstance(self.time, time):
            self.time = time_format(self.time)


class DishSaleBean:
    def __init__(self, dish_model, sales):
        self.dish_id = dish_model.id
        self.dish_name = dish_model.dish_name
        self.price = dish_model.price
        self.sales = sales


class DishBean:
    def __init__(self, dish_model):
        self.dish_id = dish_model.id
        self.window_id = dish_model.window.id
        self.dish_name = dish_model.dish_name
        self.price = dish_model.price
        self.is_heat = dish_model.is_heat
        self.description = dish_model.description
        self.img_addr = dish_model.img_addr
        self.sales = dish_model.sales
        self.grade = dish_model.grade
        if self.img_addr:
            self.img_addr = str(self.img_addr)
        else:
            self.img_addr = None


class OrderBean:
    def __init__(self, order_model, order_dish_bean_list=[]):
        self.id = order_model.id
        self.order_id = order_model.order_id
        self.customer_id = order_model.customer.id
        self.window_id = order_model.window.id
        self.building_id = order_model.building
        if self.building_id:
            self.building_id = order_model.building.id
        self.address = order_model.address
        if self.address:
            self.address = order_model.address.addr
        self.notes = order_model.notes
        self.food_cost = order_model.food_cost
        self.deliver_cost = order_model.deliver_cost
        self.order_status = order_model.order_status
        self.dish_list = order_dish_bean_list   # a list of instance of OrderDishBean
        self.create_time = order_model.create_time
        self.update_time = order_model.update_time
        self.deal_time = order_model.deal_time
        self.deliver_time = order_model.deliver_time
        if self.deliver_time:
            self.deliver_time = self.deliver_time.__unicode__()
        if self.create_time:
            self.create_time = datetime_format(convert_to_localtime(self.create_time))
        if self.update_time:
            self.update_time = datetime_format(convert_to_localtime(self.update_time))
        if self.deal_time:
            self.deal_time = datetime_format(convert_to_localtime(self.deal_time))


class OrderDetailBean(OrderBean):
    def __init__(self, order_model, order_dish_bean_list=[]):
        OrderBean.__init__(self, order_model)

        window_model = order_model.window
        self.window_name = window_model.window_name
        self.window_tel = window_model.user_name
        self.canteen_name = window_model.canteen.canteen_name

        customer_model = order_model.customer
        self.customer_tel = customer_model.user_name
        self.nick_name = customer_model.nick_name

        if self.building_id:
            building_model = order_model.building
            self.terminal_id = building_model.terminal_id
            self.building_name = building_model.building_name
            district_model = building_model.district
            self.district_name = district_model.district_name
            self.school_name = district_model.school.school_name

        self.dish_list = order_dish_bean_list  # a list of instance of OrderDishBean


class CommentBean():
    def __init__(self, order_dish_model):
        self.grade = order_dish_model.grade
        self.text = order_dish_model.text
        self.comment_time = order_dish_model.comment_time
        self.reply = order_dish_model.reply
        self.reply_time = order_dish_model.reply_time
        if self.comment_time:
            self.comment_time = datetime_format(convert_to_localtime(self.comment_time))
        if self.reply_time:
            self.reply_time = datetime_format(convert_to_localtime(self.reply_time))


class OrderDishBean(CommentBean):
    def __init__(self, order_dish_model):
        CommentBean.__init__(self, order_dish_model)
        self.id = order_dish_model.id
        self.number = order_dish_model.number

        dish_model = order_dish_model.dish
        self.dish_id = dish_model.id
        self.dish_name = dish_model.dish_name
        self.price = dish_model.price
        self.is_heat = dish_model.is_heat



