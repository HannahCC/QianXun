from django.shortcuts import render

# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from forms import LoginForm
from db import manager
from utils.Serializer import json_response, json_response_from_object
from utils.Decorator import manager_token_required, post_required, exception_handled
from utils.SendEmail import email
from utils.MakeSerialNumber import get_serial_number
from QianXun.settings import ADMIN_EMAIL
from conf.resp_code import *

# Create your views here.

def index(request):
    return render_to_response('test/testManager.html')


@exception_handled
@post_required
def manager_login(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        manager_login_dict = login_form.cleaned_data
        try:
            manager_model = manager.get_by_username(manager_login_dict)  # verify user's authority
            manager_bean = manager.update_token(manager_model)  # assign a token for user
            return json_response_from_object(OK, manager_bean)
        except ObjectDoesNotExist:
            return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
    else:
        return json_response(PARAM_REQUIRED, login_form.errors)


@exception_handled
@manager_token_required
@post_required
def customer_password_reset(request):
    customer_password_form = CustomerPasswordForm(request.POST)
    if customer_password_form.is_valid():
        customer_password_dict = customer_password_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer_bean = customer.update_password(customer_model, customer_password_dict)
        return json_response_from_object(OK, customer_bean)
    else:
        return json_response(PARAM_REQUIRED, customer_password_form.errors)
