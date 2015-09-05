__author__ = 'Hannah'

from QianXun.account.models import Customer, Address
from QianXun.account.beans import CustomerBean, BuildingBean, AddressBean
from utils.Pagination import get_paginator
from utils.MakeSerialNumber import new_token
from datetime import date
from conf.enum_value import IS_VALID


# register
def isUnregistered(user_name):
    customer_list = Customer.objects.filter(user_name__exact=user_name)
    if len(customer_list)==0:
        return True
    else:
        return False


def create(customer_dict):
    customer_model = Customer()
    customer_model.school = customer_dict['school']
    customer_model.user_name = customer_dict['user_name']
    customer_model.client_id = customer_dict['client_id']
    customer_model.registration_id = customer_dict['registration_id']
    customer_model.password = customer_dict['password']
    customer_model.user_type = customer_dict['user_type']
    customer_model.nick_name = customer_dict['nick_name']
    customer_model.version = customer_dict['version']
    customer_model.save()
    return customer_model


# token_required
def get_by_token(token):
    customer_model = Customer.objects.get(token__exact=token, is_valid=IS_VALID[1][0])
    return customer_model


# login,pwd reset
def get_by_username(customer_login_dict):
    customer_model = Customer.objects.get(user_name__exact=customer_login_dict['user_name'], is_valid=IS_VALID[1][0])
    return customer_model


# login
def update_token(customer_model, customer_login_dict):
    customer_model.client_id = customer_login_dict['client_id']
    customer_model.registration_id = customer_login_dict['registration_id']
    customer_model.version = customer_login_dict['version']
    customer_model.token = new_token()
    customer_model.save()
    return CustomerBean(customer_model)


def update_profile(customer_model, customer_profile_dict):
    customer_model.school = customer_profile_dict['school']
    customer_model.user_type = customer_profile_dict['user_type']
    customer_model.nick_name = customer_profile_dict['nick_name']
    customer_model.save()
    return customer_model


def update_password(customer_model, customer_password_dict):
    customer_model.password = customer_password_dict['new_password']
    customer_model.save()
    return customer_model


def update_username(customer_model, customer_username_dict):
    customer_model.user_name = customer_username_dict['user_name']
    customer_model.save()
    return customer_model


def delete_token(customer_model):
    customer_model.token = ''
    customer_model.save()
    return customer_model


def create_addr(customer_model, address_dict):
    customer_model.building.add(address_dict['building'])
    return customer_model


def get_user_addr(customer_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    building_list = customer_model.building.order_by('id')[paginator[0]:paginator[1]]
    addr_list = []
    for building_model in building_list:
        building_bean = BuildingBean(building_model)
        addr_list.append(building_bean)
    return addr_list


def update_addr(customer_model, address_dict):
    customer_model.building.remove(address_dict['old_building'])
    customer_model.building.add(address_dict['new_building'])
    return customer_model


def delete_addr(customer_model, address_dict):
    customer_model.building.remove(address_dict['building'])
    return customer_model


def create_custom_addr(customer_model, address_dict):
    address_model = Address()
    address_model.customer = customer_model
    address_model.addr = address_dict['addr']
    address_model.save()
    return AddressBean(address_model)


def get_user_custome_addr(customer_model, pagination_dict):
    paginator = get_paginator(pagination_dict)
    address_list = customer_model.address_set.filter(is_valid=IS_VALID[1][0]).order_by('id')[paginator[0]:paginator[1]]
    addr_list = []
    for address_model in address_list:
        address_bean = AddressBean(address_model)
        addr_list.append(address_bean)
    return addr_list


def update_custom_addr(customer_model, address_dict):
    my_address = customer_model.address_set.get(id__exact=address_dict['address'], is_valid=IS_VALID[1][0])
    my_address.addr = address_dict['addr']
    my_address.save()
    return my_address


def delete_custom_addr(customer_model, address_dict):
    my_address = customer_model.address_set.get(id__exact=address_dict['address'], is_valid=IS_VALID[1][0])
    my_address.is_valid = IS_VALID[0][0]
    my_address.save()
    return my_address


def has_vip_balance(customer_model):
    if customer_model.is_VIP and customer_model.VIP_balance and customer_model.VIP_deadline >= date.today():
        return True
    else:
        return False


def delete_all():
    impact = Customer.objects.all().delete()
    return impact