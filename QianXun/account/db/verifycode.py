__author__ = 'Hannah'
from QianXun.account.models import VerifyCode


def get_by_username_and_code(user_name, verify_code):
    verify_code_model = VerifyCode.objects.get(user_name__exact=user_name, verify_code__exact=verify_code)
    return verify_code_model


def create(verify_code):
    verify_code.save()
    return verify_code


def delete(verify_code):
    assert verify_code
    if verify_code.id:
        VerifyCode.objects.filter(id=verify_code.id).delete()
    return verify_code


def delete_by_username(user_name):
    assert user_name
    VerifyCode.objects.filter(user_name=user_name).delete()
    return user_name