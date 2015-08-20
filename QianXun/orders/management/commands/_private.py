# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from QianXun.orders.models import Orders
from conf.enum_value import ORDER_STATUS
from datetime import datetime, timedelta
from utils.MakeSerialNumber import new_batch_id, new_refund_id
import xlwt


def auto_update_order():
    # finish order ( change status from peisongzhong to daipingjia )
    now = datetime.now()
    start = now - timedelta(days=2)
    print 'here is update_order'
    number = {}
    impact = Orders.objects.filter(order_status__exact=ORDER_STATUS[5][0], update_time__lte=start). \
            update(order_status=ORDER_STATUS[7][0], update_time=datetime.now())
    number.update({'finish': impact})
    # cancel order ( change status from weifukuan to yiquxiao )
    impact = Orders.objects.filter(order_status__exact=ORDER_STATUS[1][0], update_time__lte=start). \
            update(order_status=ORDER_STATUS[4][0], update_time=datetime.now())
    number.update({'cancel': impact})
    return number


def update_order(order_list, new_status):
    for order_model in order_list:
        order_model.order_status = new_status
        order_model.save()


def display_order(order_status):
    order_list = Orders.objects.filter(order_status__exact=order_status)
    return order_list


def make_excel(order_list, note):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('batch_refund', cell_overwrite_ok=True)
    sheet.write(0, 0, u'批次号')
    sheet.write(0, 1, u'总金额（元）')
    sheet.write(0, 2, u'总笔数）')
    sheet.write(2, 0, u'商户退款流水号')
    sheet.write(2, 1, u'支付宝交易号')
    sheet.write(2, 2, u'退款金额）')
    sheet.write(2, 3, u'退款备注）')
    number = 0
    total_cost = 0
    for order_model in order_list:
        number += 1
        sheet.write(number+2, 0, new_refund_id())
        sheet.write(number+3, 1, order_model.transaction_id)
        cost = order_model.food_cost + order_model.deliver_cost
        total_cost += cost
        sheet.write(number+2, 2, cost)
        sheet.write(number+2, 3, note)
    batch_id = new_batch_id()
    sheet.write(1, 0, batch_id)
    sheet.write(1, 1, total_cost)
    sheet.write(0, 2, number)
    filename = "".join(['d:\\refund\\', str(batch_id), '.xls'])
    book.save(filename)


