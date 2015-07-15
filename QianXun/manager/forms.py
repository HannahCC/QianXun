# -*-encoding:utf-8 -*-
__author__ = 'Jeremy'

from django import forms

from conf.enum_value import LOGINTYPE


class LoginForm(forms.Form):
    user_name = forms.CharField(min_length=11, max_length=11)
    login_type = forms.ChoiceField(choices=LOGINTYPE)
    password = forms.CharField(max_length=64)


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


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)
