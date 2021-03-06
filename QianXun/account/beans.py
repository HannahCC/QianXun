__author__ = 'Hannah'
from conf.enum_value import WINDOW_STATUS

class BuildingBean:
    def __init__(self, building_model):
        self.buildingId = building_model.id
        self.terminalId = building_model.terminal_id
        self.buildingName = building_model.building_name
        district_model = building_model.district
        self.districtName = district_model.district_name
        self.schoolName = district_model.school.school_name


class AddressBean:
    def __init__(self, address_model):
        self.addressId = address_model.id
        self.address = address_model.addr


class CustomerBean:
    def __init__(self, customer_model):
        self.token = customer_model.token
        self.userType = customer_model.user_type
        self.userName = customer_model.user_name
        self.nickName = customer_model.nick_name
        school_model = customer_model.school
        self.schoolId = school_model.id
        self.schoolName = school_model.school_name


class WindowBean:
    def __init__(self, window_model):
        self.id = window_model.id
        self.token = window_model.token
        self.userName = window_model.user_name
        self.name = window_model.name
        self.windowName = window_model.window_name
        self.windowStatus = window_model.window_status
        self.windowStatusDesc = WINDOW_STATUS[window_model.window_status-1][1]
        self.imgAddr = window_model.img_addr
        self.sales = window_model.sales
        self.grade = window_model.grade
        self.commentNumber = window_model.comment_number
        self.deliverTimeNumber = window_model.deliver_time_number
        self.dishNumber = window_model.dish_number
        self.promotionNumber = window_model.promotion_number
        self.promotionList = window_model.promotion_list
        canteen_model = window_model.canteen
        self.canteenId = canteen_model.id
        self.canteenName = canteen_model.canteen_name
        school_model = window_model.school
        self.schoolId = school_model.id
        self.schoolName = school_model.school_name
        
        if self.imgAddr:
            self.imgAddr = str(self.imgAddr)
        else:
            self.imgAddr = None
