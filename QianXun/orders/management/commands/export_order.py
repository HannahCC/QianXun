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
        if len(refused_order_list)==0 and len(canceled_order_list)==0:
            print u'暂无需退款记录。'
            return
        else:
            make_excel(refused_order_list, canceled_order_list)
            print u'文件导出完成。请在“D:\\refund\\”下找到最新的退款文件，其文件名即为退款批次号。'
            print u'请在5分钟内完成订单退款操作。【5分钟后用户订单状态将改为已退款】'
            print u'请不要关闭该窗口，直到提示关闭'
            # 10 min after export data, order' status will change to refunded
            time.sleep(60*5)
            update_order(refused_order_list, ORDER_STATUS[6][0])
            update_order(canceled_order_list, ORDER_STATUS[6][0])
            print u'已更新订单状态，请关闭该窗口'
            return
