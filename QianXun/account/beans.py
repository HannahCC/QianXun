__author__ = 'Hannah'
from utils.SalesCalculator import window_sales_calculate


class BuildingBean:
    def __init__(self, building_model):
        self.building_id = building_model.id
        self.terminal_id = building_model.terminal_id
        self.building_name = building_model.building_name
        district_model = building_model.district
        self.district_name = district_model.district_name
        self.school_name = district_model.school.school_name


class AddressBean:
    def __init__(self, address_model):
        self.address_id = address_model.id
        self.address = address_model.addr


class CustomerBean:
    def __init__(self, customer_model):
        self.token = customer_model.token
        self.user_type = customer_model.user_type
        self.user_name = customer_model.user_name
        self.nick_name = customer_model.nick_name
        self.school_id = customer_model.school_id


class WindowBean:
    def __init__(self, window_model):
        self.token = window_model.token
        self.user_name = window_model.user_name
        self.name = window_model.name
        self.window_name = window_model.window_name
        self.window_status = window_model.window_status
        self.img_addr = window_model.img_addr
        self.sales = window_model.sales
        self.grade = window_model.grade
        self.comment_number = window_model.comment_number
        self.promotion_number = window_model.promotion_number
        self.dish_number = window_model.dish_number
        self.canteen_id = window_model.canteen_id

        if self.img_addr:
            self.img_addr = str(self.img_addr)
        else:
            self.img_addr = None
