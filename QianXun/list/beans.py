__author__ = 'Hannah'


class MySchool:
    def __init__(self, school_id, school_name):
        self.school_id = school_id
        self.school_name = school_name


class MyDistrict:
    def __init__(self, district_id, district_name):
        self.district_id = district_id
        self.district_name = district_name


class MyBuilding:
    def __init__(self, building_id, building_name, terminal_id):
        self.building_id = building_id
        self.building_name = building_name
        self.terminal_id = terminal_id


class MyCanteen:
    def __init__(self, canteen_id, canteen_name, img_addr, sales, grade):
        self.canteen_id = canteen_id
        self.canteen_name = canteen_name
        self.img_addr = img_addr
        self.sales = sales
        self.grade = grade


class MyProtype:
    def __init__(self, pro_type_id, pro_type_name, img_addr):
        self.pro_type_id = pro_type_id
        self.pro_type_name = pro_type_name
        self.img_addr = img_addr

