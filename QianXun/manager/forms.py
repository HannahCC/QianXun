# -*-encoding:utf-8 -*-
__author__ = 'Jeremy'

from django import forms

from conf.enum_value import LOGINTYPE, WINDOW_STATUS


class LoginForm(forms.Form):
    user_name = forms.CharField(min_length=11, max_length=11)
    login_type = forms.ChoiceField(choices=LOGINTYPE)
    password = forms.CharField(max_length=64)


class PasswordResetForm(forms.Form):
    user_name = forms.CharField(min_length=11, max_length=11)
    login_type = forms.ChoiceField(choices=LOGINTYPE)
    verify_code = forms.CharField(max_length=6)
    new_password = forms.CharField(min_length=6, max_length=64)
    new_password2 = forms.CharField(max_length=64)

    def clean_new_password2(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        password = cleaned_data.get('new_password', '')
        password2 = cleaned_data.get('new_password2', '')
        if password != password2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password2


class PasswordUpdateForm(forms.Form):
    token = forms.CharField(max_length=64)
    old_password = forms.CharField(min_length=6, max_length=64)
    new_password = forms.CharField(min_length=6, max_length=64)
    new_password2 = forms.CharField(min_length=6, max_length=64)

    def clean_new_password2(self):
        cleaned_data = super(PasswordUpdateForm, self).clean()
        password = cleaned_data.get('new_password', '')
        password2 = cleaned_data.get('new_password2', '')
        if password != password2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password2


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)
    order_by = forms.CharField(max_length=64, required=False)


class WindowVerifyForm(forms.Form):
    token = forms.CharField(max_length=64)
    window_id = forms.IntegerField()
    window_status = forms.ChoiceField(choices=WINDOW_STATUS)

    def clean_window_status(self):
        cleaned_data = super(WindowVerifyForm, self).clean()
        window_status_str = cleaned_data.get('window_status', '')
        window_status = int(window_status_str)
        if window_status!=WINDOW_STATUS[1][0] and window_status!=WINDOW_STATUS[2][0] :
            raise forms.ValidationError(u'请输入合法的窗口状态')
        return window_status_str


class SalesForm(forms.Form):
    token = forms.CharField(max_length=64)
    start_date = forms.DateField()
    end_date = forms.DateField()
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)