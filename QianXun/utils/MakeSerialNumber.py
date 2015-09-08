__author__ = 'Hannah'
from uuid import uuid4
from datetime import datetime
import calendar
import random


def new_token():
    token = uuid4().hex
    return token


def new_order_id(seed):
    """
        Make serial number
        the serial number is made up of seed(5), current_time(10), and a random number(5)
        seed can be Window_ID(5) to make order_id
        also can be Customer_ID(5) to make customer_token
        ......
    """
    seed = seed % 10000 + 10000
    now = datetime.now()
    timestamp = calendar.timegm(now.timetuple())
    random_num = random.randint(10000000, 99999999)
    serial_number = "-".join([str(timestamp), str(random_num)])
    return serial_number


def new_batch_id():
    """
        Make serial number(12-25)
        the serial number is made up of current_time(14), and a random number(5)
        ......
    """
    now = datetime.now()
    part1 = now.strftime('%Y%m%d%H%M%S')
    part2 = random.randint(10000, 99999)
    serial_number = "".join([part1, str(part2)])
    return serial_number


def new_refund_id():
    """
        Make serial number(16)
        the serial number is made up of current_time(14), and a random number(2)
        ......
    """
    now = datetime.now()
    part1 = now.strftime('%Y%m%d%H%M%S')
    part2 = random.randint(10, 99)
    serial_number = "".join([part1, str(part2)])
    return serial_number
