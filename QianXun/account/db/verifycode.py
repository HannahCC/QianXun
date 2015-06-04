__author__ = 'Hannah'
from QianXun.account.models import VerifyCode


def get_by_username_and_code(user_name, verify_code):
    verify_code_model = VerifyCode.objects.get(user_name__exact=user_name, verify_code__exact=verify_code)
    return verify_code_model


def create(verifycode_validation_dict):
    new_verify_code = VerifyCode()
    new_verify_code.user_name = verifycode_validation_dict['user_name']
    new_verify_code.verify_code = verifycode_validation_dict['verify_code']
    new_verify_code.save()
    return new_verify_code


def delete(verify_code):
    assert verify_code
    if verify_code.id:
        VerifyCode.objects.filter(id=verify_code.id).delete()
    return verify_code


def delete_by_username(user_name):
    assert user_name
    VerifyCode.objects.filter(user_name=user_name).delete()
    return user_name