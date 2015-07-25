# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from forms import LoginForm, PaginationForm, WindowVerifyForm, PasswordResetForm, PasswordUpdateForm
from QianXun.account.db import window
from QianXun.notice.db import notice
from QianXun.orders.db import dish
from QianXun.notice.forms import ChangeCNoticeForm, CreateCNoticeForm, ChangeSNoticeForm, CreateSNoticeForm
from db import manager
from utils.Serializer import json_response, json_response_from_object
from utils.Decorator import school_manager_token_required, canteen_manager_token_required, post_required,\
    exception_handled, manager_token_required, verify_code_required
from utils.SendEmail import email
from utils.MakeSerialNumber import new_order_id
from QianXun.settings import ADMIN_EMAIL
from conf.resp_code import *
from conf.enum_value import LOGINTYPE
from conf.default_value import CANTEEN_FLAG, SCHOOL_FLAG
from utils.Pagination import get_paginator

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
                school_manager_model = manager.school_get_by_username(manager_login_dict)
                if school_manager_model.password == manager_login_dict['password']:  # verify user's authority
                    manager_bean = manager.school_update_token(school_manager_model)  # assign a token for user
                    return json_response_from_object(OK, manager_bean)
                else:
                    return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
            except ObjectDoesNotExist:
                return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
        elif login_type == LOGINTYPE[1][0]:
            try:
                canteen_manager_model = manager.canteen_get_by_username(manager_login_dict)
                if canteen_manager_model.password == manager_login_dict['password']:  # verify user's authority
                    manager_bean = manager.canteen_update_token(canteen_manager_model)  # assign a token for user
                    return json_response_from_object(OK, manager_bean)
                else:
                    return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
            except ObjectDoesNotExist:
                return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
        else:
            return json_response(PARAM_REQUIRED, "LOGINTYPE Needed!")
    else:
        return json_response(PARAM_REQUIRED, login_form.errors)


@exception_handled
@manager_token_required
@post_required
def manager_password_update(request):
    manager_password_form = PasswordUpdateForm(request.POST)
    if manager_password_form.is_valid():
        manager_password_dict = manager_password_form.cleaned_data
        manager_model = request.user_meta['manager_model']
        if manager_model.password == manager_password_dict['old_password']:
            manager.update_password(manager_model, manager_password_dict)
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(USER_PWD_ERROR, CODE_MESSAGE.get(USER_PWD_ERROR))
    else:
        return json_response(PARAM_REQUIRED, manager_password_form.errors)


@exception_handled
@manager_token_required
@post_required
def manager_logout(request):
    manager_model = request.user_meta.get("manager_model")
    manager.delete_token(manager_model)
    return json_response(OK, CODE_MESSAGE.get(OK))



@exception_handled
@manager_token_required
@post_required
def view_upper_notice(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        if request.user_meta.get("flag") == CANTEEN_FLAG:
            canteen_manager = request.user_meta.get("manager_model")
            total = manager.get_upper_notice_number(canteen_manager)
            school_notice_bean_list = manager.get_upper_notice(canteen_manager, pagination_dict)
        else:
            school_manager = request.user_meta.get("manager_model")
            total = manager.get_all_school_notice_number(school_manager)
            school_notice_bean_list = manager.get_all_school_notice(school_manager, pagination_dict)
        result = {"total":total,"rows":school_notice_bean_list}
        return json_response_from_object(OK, result)
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@canteen_manager_token_required
@post_required
def view_canteen_notice(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        canteen_manager = request.user_meta.get("manager_model")
        total = manager.get_canteen_notice_number(canteen_manager)
        canteen_notice_bean_list = manager.get_canteen_notice(canteen_manager, pagination_dict)
        result = {"total":total,"rows":canteen_notice_bean_list}
        return json_response_from_object(OK, result)
    else:
         return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@manager_token_required
@post_required
def sm_find_notice_by_keyword(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        paginator = get_paginator(pagination_dict)
        search_words = request.POST.get("key_words")
        if request.user_meta.get("flag") == CANTEEN_FLAG:
            school = request.user_meta.get("manager_model").canteen.school
        else:
            school = request.user_meta.get("manager_model").school
        school_notice_bean_list = notice.find_school_notice_list_by_word(school, search_words)
        total = len(school_notice_bean_list)
        result = {"total":total,"rows":school_notice_bean_list[paginator[0]:paginator[1]]}
        return json_response_from_object(OK, result)
    else:
         return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@canteen_manager_token_required
@post_required
def cm_find_notice_by_keyword(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        paginator = get_paginator(pagination_dict)
        search_words = request.POST.get("key_words")
        canteen = request.user_meta.get("manager_model").canteen
        canteen_notice_bean_list = notice.find_canteen_notice_list_by_word(canteen, search_words)
        total = len(canteen_notice_bean_list)
        result = {"total":total,"rows":canteen_notice_bean_list[paginator[0]:paginator[1]]}
        return json_response_from_object(OK, result)
    else:
         return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@canteen_manager_token_required
@post_required
def cm_modify_own_notice(request):
    change_notice_form = ChangeCNoticeForm(request.POST)
    if change_notice_form.is_valid():
        change_notice_dict= change_notice_form.cleaned_data
        canteen_manager = request.user_meta.get("manager_model")
        notice_id = request.POST.get("notice_id")
        already_notice = notice.get_canteen_notice_by_id(notice_id)
        # 只能修改自己发布的通知
        if canteen_manager != already_notice.manager:
            return json_response(AUTHORFAILED, CODE_MESSAGE.get(AUTHORFAILED))

        notice_bean = notice.cm_modify_notice(already_notice, change_notice_dict)
        return json_response_from_object(OK, notice_bean)
    else:
        return json_response(PARAM_REQUIRED, change_notice_form.errors)


@exception_handled
@canteen_manager_token_required
@post_required
def cm_create_notice(request):
    canteen_manager = request.user_meta.get("manager_model")
    create_notice_form = CreateCNoticeForm(request.POST)
    if create_notice_form.is_valid():
        create_notice_dict= create_notice_form.cleaned_data
        notice_bean = notice.cm_create_notice(canteen_manager, create_notice_dict)
        return json_response_from_object(OK, notice_bean)
    else:
        return json_response(PARAM_REQUIRED, create_notice_form.errors)



@exception_handled
@canteen_manager_token_required
@post_required
def cm_delete_notice(request):
    canteen_manager = request.user_meta.get("manager_model")
    notice_id = request.POST.get("notice_id")
    notice_model = notice.get_canteen_notice_by_id(notice_id)
    if canteen_manager != notice_model.manager:
        return json_response(AUTHORFAILED, CODE_MESSAGE.get(AUTHORFAILED))
    notice.delte_notice(notice_model)
    return json_response(OK, CODE_MESSAGE.get(OK))


@exception_handled
@canteen_manager_token_required
@post_required
def cm_show_notice(request):
    canteen_manager = request.user_meta.get("manager_model")
    notice_bean_list = notice.find_canteen_notice_list_by_canteen_manager(canteen_manager)
    return json_response_from_object(OK, notice_bean_list)



@exception_handled
@school_manager_token_required
@post_required
def sm_modify_own_notice(request):
    change_notice_form = ChangeSNoticeForm(request.POST)
    if change_notice_form.is_valid():
        change_notice_dict= change_notice_form.cleaned_data
        school_manager = request.user_meta.get("manager_model")
        notice_id = request.POST.get("notice_id")
        already_notice = notice.get_school_notice_by_id(notice_id)
        # 只能修改自己发布的通知
        if school_manager != already_notice.manager:
            return json_response(AUTHORFAILED, CODE_MESSAGE.get(AUTHORFAILED))

        notice_bean = notice.sm_modify_notice(already_notice, change_notice_dict)
        return json_response_from_object(OK, notice_bean)
    else:
        return json_response(PARAM_REQUIRED, change_notice_form.errors)


@exception_handled
@school_manager_token_required
@post_required
def sm_create_notice(request):
    school_manager = request.user_meta.get("manager_model")
    create_notice_form = CreateSNoticeForm(request.POST)
    if create_notice_form.is_valid():
        create_notice_dict= create_notice_form.cleaned_data
        notice_bean = notice.sm_create_notice(school_manager, create_notice_dict)
        return json_response_from_object(OK, notice_bean)
    else:
        return json_response(PARAM_REQUIRED, create_notice_form.errors)



@exception_handled
@school_manager_token_required
@post_required
def sm_delete_notice(request):
    school_manager = request.user_meta.get("manager_model")
    notice_id = request.POST.get("notice_id")
    notice_model = notice.get_school_notice_by_id(notice_id)
    if school_manager != notice_model.manager:
        return json_response(AUTHORFAILED, CODE_MESSAGE.get(AUTHORFAILED))
    notice.delte_notice(notice_model)
    return json_response(OK, CODE_MESSAGE.get(OK))



@exception_handled
@school_manager_token_required
@post_required
def sm_show_notice(request):
    school_manager = request.user_meta.get("manager_model")
    notice_bean_list = notice.find_school_notice_list_by_school_manager(school_manager)
    return json_response_from_object(OK, notice_bean_list)


@exception_handled
@school_manager_token_required
@post_required
def get_school_windows(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        school_manager = request.user_meta.get("manager_model")
        total = manager.get_school_windows_number(school_manager)
        windows_list_bean = manager.get_school_windows(school_manager,pagination_dict)
        result = {"total":total,"rows":windows_list_bean}
        return json_response_from_object(OK, result)
    else:
         return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@canteen_manager_token_required
@post_required
def get_canteen_windows(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        canteen_manager = request.user_meta.get("manager_model")
        total = manager.get_canteen_windows_number(canteen_manager)
        windows_list_bean = manager.get_canteen_windows(canteen_manager,pagination_dict)
        result = {"total":total,"rows":windows_list_bean}
        return json_response_from_object(OK, result)
    else:
         return json_response(PARAM_REQUIRED, pagination_form.errors)

@exception_handled
def search_window_by_name(request):
    school_id = request.GET.get("school_id")
    canteen_id = request.GET.get("canteen_id")
    query_str = request.GET.get("q")
    window_list_bean = manager.search_canteen_by_name(school_id, canteen_id, query_str)
    return json_response_from_object(OK, window_list_bean)


@exception_handled
@manager_token_required
@post_required
def show_window_dish(request):
    window_id = request.POST.get("window_id")
    dish_list_bean = dish.get_dish_bean_list_bywin(window_id=window_id)
    return json_response_from_object(OK, dish_list_bean)


@exception_handled
@canteen_manager_token_required
@post_required
def verify_window(request):
    window_verify_form = WindowVerifyForm(request.POST)
    if window_verify_form.is_valid():
        window_verify_dict = window_verify_form.cleaned_data
        window_model = window.update_status(window_verify_dict)
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, window_verify_form.errors)