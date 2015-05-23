# -*-encoding:utf-8 -*-
__author__ = 'Jeremy'

from django import forms

from QianXun.manager.models import SchoolManager, CanteenManager
from utils.Validator import validate_phone, validate_password, validate_window_status
from conf.enum_value import LOGINTYPE

class LoginForm(forms.Form):
    user_name = forms.CharField(min_length=11, max_length=11)
    login_type = forms.ChoiceField(choices=LOGINTYPE)
    password = forms.CharField(max_length=64)

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = SchoolManager
    #     fields = ['password']



class ManagerPasswordForm(forms.Form):
    token = forms.CharField(max_length=64)
    verify_code = forms.CharField(min_length=6, max_length=6)
    password = forms.CharField(min_length=6, max_length=64)
    password2 = forms.CharField(max_length=64)

    def clean_password2(self):
        cleaned_data = self.clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', ' ')
        if password != password2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password2