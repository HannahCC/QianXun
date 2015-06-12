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
    random_num = random.randint(10000, 99999)
    serial_number = "".join([str(seed), str(timestamp), str(random_num)])
    return serial_number
