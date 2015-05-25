__author__ = 'Hannah'

from QianXun.list.models import School, District, Building, Canteen, PromotionType
from utils.Pagination import get_paginator
from QianXun.list.beans import *


def get_protype_bean_list(pagination_dict):
    paginator = get_paginator(pagination_dict)
    protype_list = PromotionType.objects.filter(is_valid=1).order_by('pro_type_name')[paginator[0]: paginator[1]]
    protype_bean_list = []
    for protype_model in protype_list:
        protype_bean_list.append(ProtypeBean(protype_model))
    return protype_bean_list


def get_school_bean_list(pagination_dict):
    paginator = get_paginator(pagination_dict)
    school_list = School.objects.filter(is_valid=1).order_by('school_name')[paginator[0]: paginator[1]]
    school_bean_list = []
    for school_model in school_list:
        school_bean_list.append(SchoolBean(school_model))
    return school_bean_list


def get_district_bean_list(school_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    district_list = District.objects.filter(school__exact=school_id, is_valid=1).order_by('district_name')[paginator[0]: paginator[1]]
    district_bean_list = []
    for district_model in district_list:
        district_bean_list.append(DistrictBean(district_model))
    return district_bean_list


def get_building_bean_list(district_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    building_list = Building.objects.filter(district__exact=district_id, is_valid=1).order_by('building_name')[paginator[0]: paginator[1]]
    building_bean_list = []
    for building_model in building_list:
        building_bean_list.append(BuildingBean(building_model))
    return building_bean_list


def get_canteen_bean_list(school_id, pagination_dict):
    paginator = get_paginator(pagination_dict)
    canteen_list = Canteen.objects.filter(school__exact=school_id, is_valid=1).order_by('canteen_name')[paginator[0]: paginator[1]]
    canteen_bean_list = []
    for canteen_model in canteen_list:
        canteen_bean_list.append(CanteenBean(canteen_model))
    return canteen_bean_list


def get_canteen_by_id(canteen_id):
    canteen_model = Canteen.objects.get(id__exact=canteen_id)
    return CanteenBean(canteen_model)