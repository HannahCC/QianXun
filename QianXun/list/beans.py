__author__ = 'Hannah'


class SchoolBean:
    def __init__(self, school_model):
        self.school_id = school_model.id
        self.school_name = school_model.school_name


class DistrictBean:
    def __init__(self, district_model):
        self.district_id = district_model.id
        self.district_name = district_model.district_name


class BuildingBean:
    def __init__(self, building_model):
        self.building_id = building_model.id
        self.building_name = building_model.building_name
        self.terminal_id = building_model.terminal_id


class CanteenBean:
    def __init__(self, canteen_model):
        self.canteen_id = canteen_model.id
        self.canteen_name = canteen_model.canteen_name
        self.img_addr = canteen_model.img_addr

        if self.img_addr:
            self.img_addr = str(self.img_addr)
        else:
            self.img_addr = None


class ProtypeBean:
    def __init__(self, pro_type_model):
        self.pro_type_id = pro_type_model.id
        self.pro_type_name = pro_type_model.pro_type_name
        self.img_addr = pro_type_model.img_addr

        if self.img_addr:
            self.img_addr = str(self.img_addr)
        else:
            self.img_addr = None

