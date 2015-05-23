# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from forms import LoginForm, ManagerPasswordForm
from db import manager
from utils.Serializer import json_response, json_response_from_object
from utils.Decorator import manager_token_required, post_required, exception_handled
from utils.SendEmail import email
from utils.MakeSerialNumber import get_serial_number
from QianXun.settings import ADMIN_EMAIL
from conf.resp_code import *
from conf.enum_value import LOGINTYPE

# Create your views here.

def index(request):
    return render_to_response('test/testManager.html')


@exception_handled
@post_required
def manager_login(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        manager_login_dict = login_form.cleaned_data
        login_type = int(manager_login_dict.get("login_type"))
        if login_type == LOGINTYPE[0][0]:   #school manager
            try:
                school_manager_model = manager.school_get_by_username(manager_login_dict)  # verify user's authority
                manager_bean = manager.school_update_token(school_manager_model)  # assign a token for user
                return json_response_from_object(OK, manager_bean)
            except ObjectDoesNotExist:
                return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
        elif login_type == LOGINTYPE[1][0]:
            try:
                canteen_manager_model = manager.canteen_get_by_username(manager_login_dict)  # verify user's authority
                manager_bean = manager.canteen_update_token(canteen_manager_model)  # assign a token for user
                return json_response_from_object(OK, manager_bean)
            except ObjectDoesNotExist:
                return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
        else:
            return json_response(PARAM_REQUIRED, "Wrong")
    else:
        return json_response(PARAM_REQUIRED, login_form.errors)


@exception_handled
@manager_token_required
@post_required
def manager_password_reset(request):
    '''
    仅支持schoolmanager修改密码，不想写canteen的
    '''
    manager_password_form = ManagerPasswordForm(request.POST)
    if manager_password_form.is_valid():
        manager_password_dict = manager_password_form.cleaned_data
        manager_model = request.user_meta['manager_model']
        manager_bean = manager.update_password(manager_model, manager_password_dict)
        return json_response_from_object(OK, manager_bean)
    else:
        return json_response(PARAM_REQUIRED, manager_password_form.errors)
