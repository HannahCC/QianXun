# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from forms import LoginForm, ManagerPasswordForm
from QianXun.notice.db import notice
from QianXun.account.db import window
from db import manager
from utils.Serializer import json_response, json_response_from_object
from utils.Decorator import school_manager_token_required, canteen_manager_token_required, post_required, exception_handled
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
@school_manager_token_required
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

@exception_handled
@canteen_manager_token_required
@post_required
def view_upper_notice(request):
    token = request.POST.get("token")
    canteen_manager = manager.canteen_get_by_token(token)
    shcool_notice_bean_list = manager.get_upper_notice(canteen_manager)
    return json_response_from_object(OK, shcool_notice_bean_list, "schoolNoticeList")


@exception_handled
@canteen_manager_token_required
@post_required
def view_canteen_notice(request):
    token = request.POST.get("token")
    canteen_manager = manager.canteen_get_by_token(token)
    canteen_notice_bean_list = manager.get_canteen_notice(canteen_manager)
    return json_response_from_object(OK, canteen_notice_bean_list, "canteenNoticeList")


@exception_handled
@school_manager_token_required
@post_required
def sm_find_notice_by_keyword(request):
    token = request.POST.get("token")
    search_words = request.POST.get("key_words")
    school = manager.school_get_by_token(token).school
    school_notice_bean_list = notice.find_school_notice_list_by_word(school, search_words)
    return json_response_from_object(OK, school_notice_bean_list)


@exception_handled
@canteen_manager_token_required
@post_required
def cm_find_notice_by_keyword(request):
    token = request.POST.get("token")
    search_words = request.POST.get("key_words")
    canteen_mangaer = manager.canteen_get_by_token(token)
    school_notice_bean_list = notice.find_school_notice_list_by_word(canteen_mangaer.canteen.school, search_words)
    canteen_notice_bean_list = notice.find_canteen_notice_list_by_word(canteen_mangaer.canteen, search_words)
    all_bean_list = school_notice_bean_list
    all_bean_list.extend(canteen_notice_bean_list)
    return json_response_from_object(OK, all_bean_list)


@exception_handled
@canteen_manager_token_required
@post_required
def view_window_info(request):
    window_id = request.POST.get("window_id")
    window_bean = window.get_by_id(window_id)
    return json_response_from_object(OK, window_bean)


@exception_handled
@canteen_manager_token_required
@post_required
def permit_window(request):
    window_id = request.POST.get("window_id")
    window_model_bean = window.permit(window_id)
    return json_response_from_object(OK, window_model_bean)


@exception_handled
@canteen_manager_token_required
@post_required
def not_permit_window(request):
    window_id = request.POST.get("window_id")
    window_model_bean = window.not_permit(window_id)
    return json_response_from_object(OK, window_model_bean)

