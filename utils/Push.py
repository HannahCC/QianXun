__author__ = 'Hannah'
import jpush
import sys
import logging
import traceback
from conf.default_value import JPUSH_APP_KEY, MASTER_SECRET
from jpush.common import JPushFailure, Unauthorized
from QianXun.settings import DEBUG

_LOGGER = logging.getLogger(__name__)


class JPush():
    def __init__(self):
        _jpush = jpush.JPush(JPUSH_APP_KEY, MASTER_SECRET)
        self.push = _jpush.create_push()

    def broadcast_by_tags(self, notification, *tag_list):
        self.push.platform = jpush.all_
        if len(tag_list) > 0:
            self.push.audience = jpush.audience(jpush.tag(tag_list),)
        else:
            self.push.audience = jpush.all_
        self.push.notification = jpush.notification(alert=notification)
        self.__push()

    def push_by_id(self, notification, registration_id):
        self.push.platform = jpush.all_
        self.push.audience = jpush.audience(jpush.registration_id(registration_id))
        self.push.notification = jpush.notification(alert=notification)
        self.__push()

    def __push(self):
        try:
            if DEBUG:
                _LOGGER.info("In Debug mode. It will not send msg for real.")
            else:
                self.push.send()
        except JPushFailure:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An JPushFailure error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.error(exception_message)
        except Unauthorized:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An Unauthorized error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.error(exception_message)
        except Exception:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An unexpected error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.error(exception_message)
        return


