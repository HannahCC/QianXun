# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
from django.core.management.base import BaseCommand
from _private import auto_update_order
from datetime import datetime
import time
import logging

_LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
    	print u'正在执行自动收货（取消）任务。该任务是日常任务，如无特殊情况，请勿关闭窗口。'
        number = auto_update_order()
        print 'Finish '+str(number.get('finish', 0))+' order by script. '+str(datetime.now())
        print 'Cancel '+str(number.get('cancel', 0))+' order by script. '+str(datetime.now())
        _LOGGER.info('Finish '+str(number.get('finish', 0))+' order by script. '+str(datetime.now()))
        _LOGGER.info('Cancel '+str(number.get('cancel', 0))+' order by script. '+str(datetime.now()))