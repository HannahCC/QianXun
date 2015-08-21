# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from QianXun.orders.models import Orders
from conf.enum_value import ORDER_STATUS
from datetime import datetime, timedelta
from utils.MakeSerialNumber import new_batch_id, new_refund_id
import csv


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
    batch_id = new_batch_id()
    filename = "".join(['d:\\refund\\', str(batch_id), '.csv'])
    csvf = file(filename, 'wb')
    writer = csv.writer(csvf)
    writer.writerow(['批次号'.decode('utf-8').encode('gb2312'), '总金额（元）'.decode('utf-8').encode('gb2312'), '总笔数'.decode('utf-8').encode('gb2312')])
    number = 0
    total_cost = 0
    data = []
    for order_model in order_list:
        number += 1
        cost = order_model.food_cost + order_model.deliver_cost
        total_cost += cost
        data.append((new_refund_id(), order_model.transaction_id, cost, note.decode('utf-8').encode('gb2312')))
    writer.writerow([batch_id, str(total_cost), str(number)])
    writer.writerow(['商户退款流水号'.decode('utf-8').encode('gb2312'), '支付宝交易号'.decode('utf-8').encode('gb2312'),
                     '退款金额'.decode('utf-8').encode('gb2312'), '退款备注'.decode('utf-8').encode('gb2312')])
    writer.writerows(data)
    csvf.close()