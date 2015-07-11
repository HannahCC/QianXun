__author__ = 'Hannah'


class SchoolBean:
    def __init__(self, school_model):
        self.schoolId = school_model.id
        self.schoolName = school_model.school_name


class DistrictBean:
    def __init__(self, district_model):
        self.districtId = district_model.id
        self.districtName = district_model.district_name


class BuildingBean:
    def __init__(self, building_model):
        self.buildingId = building_model.id
        self.buildingName = building_model.building_name
        self.terminalId = building_model.terminal_id


class CanteenBean:
    def __init__(self, canteen_model):
        self.canteenId = canteen_model.id
        self.canteenName = canteen_model.canteen_name


class ProtypeBean:
    def __init__(self, pro_type_model):
        self.proTypeId = pro_type_model.id
        self.proTypeName = pro_type_model.pro_type_name
        self.imgAddr = pro_type_model.img_addr

        if self.imgAddr:
            self.imgAddr = str(self.imgAddr)
        else:
            self.imgAddr = None

