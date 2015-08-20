# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from django.core.management.base import BaseCommand
from conf.enum_value import ORDER_STATUS
from _private import display_order, update_order, make_excel
import time
import logging

_LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print u'正在导出批量退款文件 ...'
        refused_order_list = display_order(ORDER_STATUS[3][0])
        canceled_order_list = display_order(ORDER_STATUS[4][0])
        make_excel(refused_order_list, u'【已拒绝】订单退款')
        make_excel(canceled_order_list, u'【已取消】订单退款')
        print u'文件导出完成。请在“D:\\refund\\”下找到最新的两个文件，分别存储了已拒绝订单和已取消订单的信息。'
        print u'请在10分钟内完成订单退款操作。【10分钟后用户订单状态将改为已退款】'
        # 10 min after export data, order' status will change to refunded
        time.sleep(60*10)
        update_order(refused_order_list, ORDER_STATUS[6][0])
        update_order(canceled_order_list, ORDER_STATUS[6][0])
