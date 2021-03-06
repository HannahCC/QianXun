# -*- coding:utf-8 -*-
from smtplib import SMTPAuthenticationError

from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from forms import WindowForm, WindowProfileForm, WindowProfileImageForm, LoginForm, PasswordResetForm,\
    PasswordUpdateForm, UsernameForm, FeedbackForm
from db import window
from QianXun.utils.Serializer import json_response, json_response_from_object
from QianXun.utils.Decorator import window_token_required, post_required, exception_handled, verify_code_required
from QianXun.utils.SendEmail import email
from QianXun.settings import ADMIN_EMAIL
from conf.resp_code import *


def index(request):
    return render_to_response('test/testWindow.html')


@exception_handled
@verify_code_required
@post_required
def window_register(request):
    window_form = WindowForm(request.POST)
    if window_form.is_valid():
        window_dict = window_form.cleaned_data
        if window.isUnregistered(window_dict['user_name']):
            window_model = window.create(window_form, False)
            window_model.user_name = window_dict['user_name']
            window_model.school = window_dict['canteen'].school
            window.create(window_model)
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(USER_REGISTERED, CODE_MESSAGE.get(USER_REGISTERED))
    else:
        return json_response(PARAM_REQUIRED, window_form.errors)


@exception_handled
@post_required
def window_login(request):
    window_login_form = LoginForm(request.POST)
    if window_login_form.is_valid():
        window_login_dict = window_login_form.cleaned_data
        try:
            window_model = window.get_by_username(window_login_dict)
            if window_model.password == window_login_dict['password']:  # verify user's authority
                window_bean = window.update_token(window_model, window_login_dict)  # assign a token for user
                return json_response_from_object(OK, window_bean)
            else:
                return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
        except ObjectDoesNotExist:
            return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
    else:
        return json_response(PARAM_REQUIRED, window_login_form.errors)


@exception_handled
@verify_code_required
@post_required
def window_password_reset(request):
    window_password_form = PasswordResetForm(request.POST)
    if window_password_form.is_valid():
        window_password_dict = window_password_form.cleaned_data
        try:
            window_model = window.get_by_username(window_password_dict)  # verify user's authority
            window.update_password(window_model, window_password_dict)
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        except ObjectDoesNotExist:
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
    else:
        return json_response(PARAM_REQUIRED, window_password_form.errors)


@exception_handled
@window_token_required
@post_required
def window_logout(request):
    window_model = request.user_meta['window_model']
    window.delete_token(window_model)
    return json_response(OK, CODE_MESSAGE.get(OK))


@exception_handled
@window_token_required
@post_required
def window_profile_display(request):
    window_model = request.user_meta['window_model']
    window_bean = window.window_model_to_bean(window_model)
    return json_response_from_object(OK, window_bean)


@exception_handled
@window_token_required
@post_required
def window_profile_update(request):
    window_profile_form = WindowProfileForm(request.POST)
    if window_profile_form.is_valid():
        window_profile_dict = window_profile_form.cleaned_data
        window_model = request.user_meta['window_model']
        window.update_profile(window_model, window_profile_dict)
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, window_profile_form.errors)


@exception_handled
@window_token_required
@post_required
def window_profile_image_update(request):
    window_profile_form = WindowProfileImageForm(request.POST, request.FILES)
    if window_profile_form.is_valid():
        window_profile_dict = window_profile_form.cleaned_data
        window_model = request.user_meta['window_model']
        window_model = window.update_profile_image(window_model, window_profile_dict)
        result = {"ImgAddr": str(window_model.img_addr)}
        return json_response(OK, result)
    else:
        return json_response(PARAM_REQUIRED, window_profile_form.errors)


@exception_handled
@window_token_required
@post_required
def window_password_update(request):
    window_password_form = PasswordUpdateForm(request.POST)
    if window_password_form.is_valid():
        window_password_dict = window_password_form.cleaned_data
        window_model = request.user_meta['window_model']
        if window_model.password == window_password_dict['old_password']:
            window.update_password(window_model, window_password_dict)
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(USER_PWD_ERROR, CODE_MESSAGE.get(USER_PWD_ERROR))
    else:
        return json_response(PARAM_REQUIRED, window_password_form.errors)


@exception_handled
@window_token_required
@verify_code_required
@post_required
def window_username_reset(request):
    window_username_form = UsernameForm(request.POST)
    if window_username_form.is_valid():
        window_username_dict = window_username_form.cleaned_data
        window_model = request.user_meta['window_model']
        window.update_username(window_model, window_username_dict)
        verify_code_model = request.verify_code_meta['verify_code_model']
        verify_code_model.delete()
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, window_username_form.errors)


@exception_handled
@window_token_required
@post_required
def window_feedback(request):
    feedback_form = FeedbackForm(request.POST)
    if feedback_form.is_valid():
        feedback_dict = feedback_form.cleaned_data
        window_id = request.user_meta['window_model'].id
        try:
            if feedback_dict['type'] == '1':  # suggestion
                feedback_dict['subject'] = "".join([u'[校园便当_商家用户反馈]', feedback_dict['subject']])
                feedback_dict['message'] = "\n----------\nfrom ID: ".join([feedback_dict['message'], str(window_id)])
                email(feedback_dict, ADMIN_EMAIL['MANAGER_EMAIL'])
            else:  # crash report
                feedback_dict['subject'] = "".join([u'[校园便当_商家版崩溃报告]', feedback_dict['subject']])
                feedback_dict['message'] = "\n----------\nfrom ID: ".join([feedback_dict['message'], str(window_id)])
                email(feedback_dict, ADMIN_EMAIL['APP_DEVELPOER_EMAIL'])
            return json_response(OK, CODE_MESSAGE.get(OK))
        except SMTPAuthenticationError:
            return json_response(EMAIL_SEND_FAILED, CODE_MESSAGE.get(EMAIL_SEND_FAILED))
    else:
        return json_response(PARAM_REQUIRED, feedback_form.errors)

