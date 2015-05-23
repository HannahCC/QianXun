__author__ = 'Hannah'
from QianXun.account.models import VerifyCode


def get_by_username(user_name):
    assert user_name
    verify_code = VerifyCode.objects.filter(user_name=user_name)
    return verify_code


def create(verify_code):
    assert verify_code
    verify_code.save()
    print(verify_code.code)
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