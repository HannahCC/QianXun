__author__ = 'Hannah'
from django.core.management.base import BaseCommand
from _private import update_order
from datetime import datetime
import time
import logging

_LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            time.sleep(60*60*24)
            number = update_order()
            print 'Finish '+str(number.get('finish', 0))+' order by script once '+str(datetime.now())
            print 'Cancel '+str(number.get('cancel', 0))+' order by script once '+str(datetime.now())
            _LOGGER.info('Finish '+str(number.get('finish', 0))+' order by script once '+str(datetime.now()))
            _LOGGER.info('Cancel '+str(number.get('cancel', 0))+' order by script once '+str(datetime.now()))
