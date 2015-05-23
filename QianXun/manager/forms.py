# -*-encoding:utf-8 -*-
__author__ = 'Jeremy'

from django import forms

from QianXun.manager.models import SchoolManager, CanteenManager
from utils.Validator import validate_phone, validate_password, validate_window_status
from conf.enum_value import FEEDBACK_TYPE

class LoginForm(forms.ModelForm):
    user_name = forms.CharField(min_length=11, max_length=11)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SchoolManager
        fields = ['password']