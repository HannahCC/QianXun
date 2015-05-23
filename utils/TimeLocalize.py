__author__ = 'Hannah'

from QianXun.settings import TIME_ZONE
import pytz
import time


def localize_time(data):
    if hasattr(data, 'create_time') and data.create_time:
        data.create_time = convert_to_localtime(data.create_time)
    if hasattr(data, 'update_time') and data.update_time:
        data.update_time = convert_to_localtime(data.update_time)
    if hasattr(data, 'deal_time') and data.deal_time:
        data.deal_time = convert_to_localtime(data.deal_time)
    if hasattr(data, 'deliver_time') and data.deliver_time:
        data.deliver_time = convert_to_localtime(data.deliver_time)
    return data


def convert_to_localtime(utc_time):
    tz = pytz.timezone(TIME_ZONE)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
    return local_time


def datetime_format(my_datetime):
    format_timestr = my_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return format_timestr


def time_format(my_time):
    format_timestr = my_time.strftime('%H:%M:%S')
    return format_timestr