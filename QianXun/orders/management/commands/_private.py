__author__ = 'Hannah'
from QianXun.orders.models import Orders
from conf.enum_value import ORDER_STATUS
from datetime import datetime, timedelta


def update_order():
    # finish order ( change status from peisongzhong to daipingjia )
    now = datetime.now()
    start = now - timedelta(days=2)
    print 'here is update_order'
    number = {}
    impact = Orders.objects.filter(order_status__exact=ORDER_STATUS[5][0], update_time__lte=start, is_valid2customer=1). \
            update(order_status=ORDER_STATUS[7][0], update_time=datetime.now())
    number.update({'finish': impact})
    # cancel order ( change status from yifukuan to yiquxiao )
    impact = Orders.objects.filter(order_status__exact=ORDER_STATUS[1][0], update_time__lte=start, is_valid2customer=1). \
            update(order_status=ORDER_STATUS[4][0], update_time=datetime.now())
    number.update({'cancel': impact})
    return number