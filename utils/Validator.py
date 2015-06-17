# -*- encoding:utf-8 -*-
__author__ = 'Hannah'
import re
from PIL import Image
from conf.enum_value import WINDOW_STATUS, ORDER_STATUS

from django.core.exceptions import ValidationError


def validate_phone(value):
    if len(value) != 11:
        raise ValidationError(u'联系方式的长度应该为11位')
    if not value.isdigit():
        raise ValidationError(u'联系方式应该由纯数字组成')


def validate_password(value):
    if len(value) < 6:
        raise ValidationError(u'请输入长度超过6位的密码')
    if not value.isalnum():
        raise ValidationError(u'请输入只含有字母和数字的密码')
    if value.isdigit():
        raise ValidationError(u'请输入含有字母的密码')


def validate_window_status(value):
    # 商家只能将自己的状态改为4：正常营业或5：歇业, 或出于1：未审核的默认状态
    if value == WINDOW_STATUS[1][0] or value == WINDOW_STATUS[2][0]:
        raise ValidationError(u'请输入合法的窗口状态')


def validate_customer_order_status(value):
    order_status = int(value)
    if order_status == ORDER_STATUS[1][0] or order_status == ORDER_STATUS[2][0] or order_status == ORDER_STATUS[6][0]:
        return value
    else:
        raise ValidationError(u'请输入合法的订单状态<权限错误>')


def validate_window_order_status(value):
    order_status = int(value)
    if order_status == ORDER_STATUS[3][0] or order_status == ORDER_STATUS[4][0] or order_status == ORDER_STATUS[5][0]:
        return value
    else:
        raise ValidationError(u'请输入合法的订单状态<权限错误>')


def validate_image(image):
    if image:
        if image.size > 500*1024:
            raise ValidationError(u"请上传小于500k的图片")
        return image
    else:
        raise ValidationError(u'读取图片失败')


def validate_order_status(old_order_status, new_order_status):
    old_order_status = int(old_order_status)
    new_order_status = int(new_order_status)
    if old_order_status % 10 != 0:  # 不能改变处于完成态的状态（末尾数为0表示处于完成态）
        # 获取两个状态的首位数字，因为状态只能依次从   x(y1)状态  -->  (x+1)(y2)状态
        while new_order_status > 10:
            new_order_status /= 10
        while old_order_status > 10:
            old_order_status /= 10
        if new_order_status - old_order_status == 1:
            return True
    return False


def validate_pro_type(pro_type, rules):
    if pro_type.pro_type_name == u'满减':  # 满x减y, x、y为整数
        match = re.search(ur"([\u4e00-\u9fa5]+)\d+([\u4e00-\u9fa5]+)\d+", rules)
        if match and match.group(1) == u'满' and match.group(2) == u'减':
            return True
        else:
            return False
    elif pro_type.pro_type_name == u'满赠':   # 满x赠y， x为整数
        match = re.search(ur"([\u4e00-\u9fa5]+)\d+([\u4e00-\u9fa5]+)\d*", rules)
        if match and match.group(1) == u'满'and match.group(2).startswith(u'赠') and not rules.endswith(u'赠') :
            return True
        else:
            return False
    return True


