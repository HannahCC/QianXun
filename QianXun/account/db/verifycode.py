__author__ = 'Hannah'
from QianXun.account.models import VerifyCode
from datetime import datetime


def get_by_username(user_name):
    verify_code_model_list = VerifyCode.objects.filter(user_name__exact=user_name) # not sure if it is exist.
    return verify_code_model_list

def get_by_username_and_code(user_name, verify_code):
    verify_code_model = VerifyCode.objects.get(user_name__exact=user_name, verify_code__exact=verify_code)
    return verify_code_model


def create(verifycode_validation_dict):
    new_verify_code = VerifyCode()
    new_verify_code.user_name = verifycode_validation_dict['user_name']
    new_verify_code.verify_code = verifycode_validation_dict['verify_code']
    new_verify_code.save()
    return new_verify_code

def update(verifycode_validation_dict):
    impact = VerifyCode.objects.filter(user_name__exact=verifycode_validation_dict['user_name']).update(
        verify_code=verifycode_validation_dict['verify_code'], create_time = datetime.now())
    return impact