# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from django.core.mail import send_mail
from QianXun.settings import EMAIL_HOST_USER


def email(email_dict, send_to):
    send_mail(email_dict['subject'], email_dict['message'], EMAIL_HOST_USER, send_to, fail_silently=False)
