__author__ = 'Hannah'
from utils.TimeLocalize import convert_to_localtime, datetime_format, time_format
from datetime import time


class PromotionBean:
    def __init__(self, promotion_model):
        self.promotionId = promotion_model.id
        self.proTypeId = promotion_model.pro_type.id
        self.rules = promotion_model.rules


class DeliverTimeBean:
    def __init__(self, deliver_time_model):
        self.deliverTimeId = deliver_time_model.id
        self.date = deliver_time_model.date
        self.time = deliver_time_model.show_time()
        if isinstance(self.time, time):
            self.time = time_format(self.time)


class DishSaleBean:
    def __init__(self, dish_model, sales):
        self.dishId = dish_model.id
        self.dishName = dish_model.dish_name
        self.isValid = dish_model.is_valid
        self.price = dish_model.price
        self.sales = sales


class DishBean:
    def __init__(self, dish_model):
        self.dishId = dish_model.id
        self.windowId = dish_model.window.id
        self.dishName = dish_model.dish_name
        self.price = dish_model.price
        self.isHeat = dish_model.is_heat
        self.description = dish_model.description
        self.imgAddr = dish_model.img_addr
        self.sales = dish_model.sales
        self.grade = dish_model.grade
        self.commentNumber = dish_model.comment_number
        if self.imgAddr:
            self.imgAddr = str(self.imgAddr)
        else:
            self.imgAddr = None


class OrderBean:
    def __init__(self, order_model, order_dish_bean_list=[]):
        if not order_dish_bean_list:
            order_dish_bean_list = []
        self.id = order_model.id
        self.orderId = order_model.order_id
        self.orderStatus = order_model.order_status
        self.notes = order_model.notes
        self.promotionList = order_model.promotion_list
        self.discount = order_model.discount
        self.foodCost = order_model.food_cost
        self.deliverCost = order_model.deliver_cost
        self.deliverTime = order_model.deliver_time
        if self.deliverTime:
            self.deliverTime = self.deliverTime.__unicode__()
        self.updateTime = order_model.update_time
        if self.updateTime:
            self.updateTime = datetime_format(convert_to_localtime(self.updateTime))
        self.dishList = order_dish_bean_list   # a list of instance of OrderDishBean

        window_model = order_model.window
        self.windowId = window_model.id
        self.windowName = window_model.window_name
        self.windowTel = window_model.user_name
        self.canteenName = window_model.canteen.canteen_name

        customer_model = order_model.customer
        self.customerId = customer_model.id
        self.customerTel = customer_model.user_name
        self.nickName = customer_model.nick_name


class OrderDetailBean(OrderBean):
    def __init__(self, order_model, order_dish_bean_list=[]):
        OrderBean.__init__(self, order_model, order_dish_bean_list)

        self.buildingId = order_model.building
        if self.buildingId:
            self.buildingId = order_model.building.id
            building_model = order_model.building
            self.terminalId = building_model.terminal_id
            self.buildingName = building_model.building_name
            district_model = building_model.district
            self.districtName = district_model.district_name
            self.schoolName = district_model.school.school_name

        self.address = order_model.address
        if self.address:
            self.address = order_model.address.addr

        self.createTime = order_model.create_time
        self.dealTime = order_model.deal_time
        if self.createTime:
            self.createTime = datetime_format(convert_to_localtime(self.createTime))
        if self.dealTime:
            self.dealTime = datetime_format(convert_to_localtime(self.dealTime))


class CommentBean():
    def __init__(self, order_dish_model):
        self.grade = order_dish_model.grade
        self.text = order_dish_model.text
        self.commentTime = order_dish_model.comment_time
        self.reply = order_dish_model.reply
        self.replyTime = order_dish_model.reply_time
        if self.commentTime:
            self.commentTime = datetime_format(convert_to_localtime(self.commentTime))
        if self.replyTime:
            self.replyTime = datetime_format(convert_to_localtime(self.replyTime))


class OrderDishBean(CommentBean):
    def __init__(self, order_dish_model):
        CommentBean.__init__(self, order_dish_model)
        self.id = order_dish_model.id
        self.number = order_dish_model.number

        dish_model = order_dish_model.dish
        self.dishId = dish_model.id
        self.dishName = dish_model.dish_name
        self.price = dish_model.price
        self.isHeat = dish_model.is_heat



