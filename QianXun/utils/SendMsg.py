# -*- coding: UTF-8 -*-
__author__ = 'Hannah'
import logging

import requests

from conf.default_value import MOB_APP_KEY, MOB_URL
from QianXun.settings import ADMIN_EMAIL
from QianXun.utils.SendEmail import email


_LOGGER = logging.getLogger(__name__)


class MobSMS:
    def __init__(self):
        self.appkey = MOB_APP_KEY
        self.verify_url = MOB_URL
        self.session = requests.Session()

    def verify_sms_code(self, zone, phone, code):
        body = {'appkey': self.appkey, 'phone': phone, 'zone': zone, 'code': code}
        res = self.session.post(self.verify_url, data=body, verify=False)
        if res.status_code == 200:  # success to link sever
            res_json = res.json()
            status = res_json.get('status', 500)
            if status == 526:
                email_content = {}
                email_content.update({'subject': u'[校园便当_服务端报告]'})
                email_content.update({'message': u'Mob短信服务器余额不足，请立即充值'})
                email(email_content, ADMIN_EMAIL['MANAGER_EMAIL'])
                exception_message = 'An MobSMS error occurred: %s' % res_json
                _LOGGER.error(exception_message)
            elif 520 >= status >= 500:
                exception_message = 'An MobSMS error occurred: %s' % res_json
                _LOGGER.info(exception_message)
            return res_json
        else:
            exception_message = "An MobSMS error occurred: {'status', 500}"
            _LOGGER.error(exception_message)
            return {'status', 500}

if __name__ == '__main__':
    mobsms = MobSMS()
    print mobsms.verify_sms_code(86, 13900000000, '1234')