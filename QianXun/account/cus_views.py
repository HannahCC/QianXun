# -*- coding:utf-8 -*-
from smtplib import SMTPAuthenticationError

from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from QianXun.settings import ADMIN_EMAIL
from conf.resp_code import *
from QianXun.utils.Serializer import json_response, json_response_from_object
from QianXun.utils.Decorator import customer_token_required, exception_handled, post_required, verify_code_required
from QianXun.utils.SendEmail import email
from forms import CustomerForm, CustomerProfileForm, LoginForm, PasswordResetForm, PasswordUpdateForm, UsernameForm, \
    FeedbackForm, PaginationForm, BuildingForm, BuildingUpdateForm, AddressForm, AddressUpdateForm, AddressDeleteForm
from db import customer
from beans import CustomerBean


def index(request):
    return render_to_response('test/testCustomer.html')


@exception_handled
@verify_code_required
@post_required
def customer_register(request):
    customer_form = CustomerForm(request.POST)
    if customer_form.is_valid():
        customer_dict = customer_form.cleaned_data
        if customer.isUnregistered(customer_dict['user_name']):
            customer.create(customer_dict)
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(USER_REGISTERED, CODE_MESSAGE.get(USER_REGISTERED))
    else:
        return json_response(PARAM_REQUIRED, customer_form.errors)


@exception_handled
@post_required
def customer_login(request):
    customer_login_form = LoginForm(request.POST)
    if customer_login_form.is_valid():
        customer_login_dict = customer_login_form.cleaned_data
        try:
            customer_model = customer.get_by_username(customer_login_dict)
            if customer_model.password == customer_login_dict['password']:  # verify user's authority
                customer_bean = customer.update_token(customer_model, customer_login_dict)  # assign a token for user
                return json_response_from_object(OK, customer_bean)
            else:
                return json_response(USER_LOGIN_FAILED, CODE_MESSAGE.get(USER_LOGIN_FAILED))
        except ObjectDoesNotExist:
            return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
    else:
        return json_response(PARAM_REQUIRED, customer_login_form.errors)


@exception_handled
@verify_code_required
@post_required
def customer_password_reset(request):
    customer_password_form = PasswordResetForm(request.POST)
    if customer_password_form.is_valid():
        customer_password_dict = customer_password_form.cleaned_data
        try:
            customer_model = customer.get_by_username(customer_password_dict)  # verify user's authority
            customer.update_password(customer_model, customer_password_dict)
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        except ObjectDoesNotExist:
            verify_code_model = request.verify_code_meta['verify_code_model']
            verify_code_model.delete()
            return json_response(USER_NOT_EXIST, CODE_MESSAGE.get(USER_NOT_EXIST))
    else:
        return json_response(PARAM_REQUIRED, customer_password_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_logout(request):
    customer_model = request.user_meta['customer_model']
    customer.delete_token(customer_model)
    return json_response(OK, CODE_MESSAGE.get(OK))


@exception_handled
@customer_token_required
@post_required
def customer_profile_display(request):
    customer_model = request.user_meta['customer_model']
    customer_bean = CustomerBean(customer_model)
    return json_response_from_object(OK, customer_bean)


@exception_handled
@customer_token_required
@post_required
def customer_profile_update(request):
    customer_profile_form = CustomerProfileForm(request.POST)
    if customer_profile_form.is_valid():
        customer_profile_dict = customer_profile_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.update_profile(customer_model, customer_profile_dict)
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, customer_profile_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_password_update(request):
    customer_password_form = PasswordUpdateForm(request.POST)
    if customer_password_form.is_valid():
        customer_password_dict = customer_password_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        if customer_model.password == customer_password_dict['old_password']:
            customer.update_password(customer_model, customer_password_dict)
            return json_response_from_object(OK, CODE_MESSAGE.get(OK))
        else:
            return json_response(USER_PWD_ERROR, CODE_MESSAGE.get(USER_PWD_ERROR))
    else:
        return json_response(PARAM_REQUIRED, customer_password_form.errors)


@exception_handled
@customer_token_required
@verify_code_required
@post_required
def customer_username_reset(request):
    customer_username_form = UsernameForm(request.POST)
    if customer_username_form.is_valid():
        customer_username_dict = customer_username_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.update_username(customer_model, customer_username_dict)
        verify_code_model = request.verify_code_meta['verify_code_model']
        verify_code_model.delete()
        return json_response_from_object(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, customer_username_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_feedback(request):
    feedback_form = FeedbackForm(request.POST)
    if feedback_form.is_valid():
        feedback_dict = feedback_form.cleaned_data
        customer_id = request.user_meta['customer_model'].id
        try:
            if feedback_dict['type'] == '1':  # suggestion
                feedback_dict['subject'] = "".join([u'[校园便当_买家用户反馈]', feedback_dict['subject']])
                feedback_dict['message'] = "\n----------\nfrom ID: ".join([feedback_dict['message'], str(customer_id)])
                email(feedback_dict, ADMIN_EMAIL['MANAGER_EMAIL'])
            else:  # crash report
                feedback_dict['subject'] = "".join([u'[校园便当_买家版崩溃报告]', feedback_dict['subject']])
                feedback_dict['message'] = "\n----------\nfrom ID: ".join([feedback_dict['message'], str(customer_id)])
                email(feedback_dict, ADMIN_EMAIL['APP_DEVELPOER_EMAIL'])
            return json_response(OK, CODE_MESSAGE.get(OK))
        except SMTPAuthenticationError:
            return json_response(EMAIL_SEND_FAILED, CODE_MESSAGE.get(EMAIL_SEND_FAILED))
    else:
        return json_response(PARAM_REQUIRED, feedback_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_addr_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        building_list = customer.get_user_addr(customer_model, pagination_dict)
        return json_response_from_object(OK, building_list, 'buildingList')
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_addr_create(request):
    address_form = BuildingForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.create_addr(customer_model, address_dict)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_addr_update(request):
    address_form = BuildingUpdateForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.update_addr(customer_model, address_dict)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_addr_delete(request):
    address_form = BuildingForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.delete_addr(customer_model, address_dict)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_custom_addr_display(request):
    pagination_form = PaginationForm(request.POST)
    if pagination_form.is_valid():
        pagination_dict = pagination_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        address_list = customer.get_user_custome_addr(customer_model, pagination_dict)
        return json_response_from_object(OK, address_list, 'addressList')
    else:
        return json_response(PARAM_REQUIRED, pagination_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_custom_addr_create(request):
    address_form = AddressForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        addr_bean = customer.create_custom_addr(customer_model, address_dict)
        return json_response_from_object(OK, addr_bean)
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_custom_addr_update(request):
    address_form = AddressUpdateForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.update_custom_addr(customer_model, address_dict)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)


@exception_handled
@customer_token_required
@post_required
def customer_custom_addr_delete(request):
    address_form = AddressDeleteForm(request.POST)
    if address_form.is_valid():
        address_dict = address_form.cleaned_data
        customer_model = request.user_meta['customer_model']
        customer.delete_custom_addr(customer_model, address_dict)
        return json_response(OK, CODE_MESSAGE.get(OK))
    else:
        return json_response(PARAM_REQUIRED, address_form.errors)




