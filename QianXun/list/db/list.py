__author__ = 'Hannah'

from QianXun.list.models import School, District, Building, Canteen, PromotionType


def get_protype_list(page, count):
    assert page >= 1
    assert count >= 1
    start = (page-1)*count
    end = start+count
    protype_list = PromotionType.objects.filter(is_valid=1).order_by('pro_type_name')[start: end]
    return protype_list


def get_school_list(page, count):
    assert page >= 1
    assert count >= 1
    start = (page-1)*count
    end = start+count
    school_list = School.objects.filter(is_valid=1).order_by('school_name')[start: end]
    return school_list


def get_district_list(school_id, page, count):
    assert school_id
    assert page >= 1
    assert count >= 1
    start = (page-1)*count
    end = start+count
    district_list = District.objects.filter(school__exact=school_id, is_valid=1).order_by('district_name')[start: end]
    return district_list

def get_building_list(district_id, page, count):
    assert district_id
    assert page >= 1
    assert count >= 1
    start = (page-1)*count
    end = start+count
    building_list = Building.objects.filter(district__exact=district_id, is_valid=1).order_by('building_name')[start: end]
    return building_list


def get_canteen_list(school_id, page, count):
    assert school_id
    assert page >= 1
    assert count >= 1
    start = (page-1)*count
    end = start+count
    canteen_list = Canteen.objects.filter(school__exact=school_id, is_valid=1).order_by('canteen_name')[start: end]
    return canteen_list