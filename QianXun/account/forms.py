# -*-encoding:utf-8 -*-
__author__ = 'Hannah'

from django import forms
from QianXun.account.models import Window, Customer
from utils.Validator import validate_phone, validate_password, validate_window_status, validate_image
from conf.enum_value import FEEDBACK_TYPE


class WindowForm(forms.ModelForm):
    password2 = forms.CharField(max_length=64)
    verify_code = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super(WindowForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].validators.append(validate_phone)
        self.fields['password'].validators.append(validate_password)

    class Meta:
        model = Window
        fields = ['canteen', 'user_name', 'name', 'password', 'window_name', 'registration_id', 'client_id', 'version']

    def clean_password2(self):
        cleaned_data = super(WindowForm, self).clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password2


class WindowProfileForm(forms.ModelForm):
    token = forms.CharField(max_length=64)
    window_name = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(WindowProfileForm, self).__init__(*args, **kwargs)
        self.fields['window_status'].validators.append(validate_window_status)
        self.fields['img_addr'].validators.append(validate_image)

    class Meta:
        model = Window
        fields = ['canteen', 'name', 'window_status', 'img_addr']


class CustomerForm(forms.ModelForm):
    password2 = forms.CharField(max_length=64)
    verify_code = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].validators.append(validate_phone)
        self.fields['password'].validators.append(validate_password)

    class Meta:
        model = Customer
        fields = ['school', 'user_type', 'user_name', 'nick_name', 'password', 'client_id', 'registration_id', 'version']

    def clean_password2(self):
        cleaned_data = super(CustomerForm, self).clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError(u'两次密码输入不一致')
        return password2


class CustomerProfileForm(forms.ModelForm):
    token = forms.CharField(max_length=64)
    nick_name = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(CustomerProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Customer
        fields = ['school', 'user_type']


class LoginForm(forms.Form):
    user_name = forms.CharField(min_length=11, max_length=11)
    password = forms.CharField(min_length=6, max_length=64)
    client_id = forms.CharField(max_length=64)
    version = forms.CharField(max_length=64)
    registration_id = forms.CharField(max_length=64)


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


class PasswordResetForm(forms.Form):
    token = forms.CharField(max_length=64)
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


class UsernameForm(forms.Form):
    token = forms.CharField(max_length=64)
    verify_code = forms.CharField(max_length=6)
    user_name = forms.CharField(min_length=11, max_length=11)

    def __init__(self, *args, **kwargs):
        super(UsernameForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].validators.append(validate_phone)


class FeedbackForm(forms.Form):
    token = forms.CharField(max_length=64)
    type = forms.ChoiceField(choices=FEEDBACK_TYPE)
    subject = forms.CharField(max_length=64)
    message = forms.CharField(max_length=1024, widget=forms.Textarea)


class BuildingForm(forms.Form):
    token = forms.CharField(max_length=64)
    building = forms.IntegerField()


class BuildingUpdateForm(forms.Form):
    token = forms.CharField(max_length=64)
    new_building = forms.IntegerField()
    old_building = forms.IntegerField()


class AddressForm(forms.Form):
    token = forms.CharField(max_length=64)
    addr = forms.CharField(max_length=64)


class AddressUpdateForm(forms.Form):
    token = forms.CharField(max_length=64)
    address = forms.IntegerField()
    addr = forms.CharField(max_length=64)


class AddressDeleteForm(forms.Form):
    token = forms.CharField(max_length=64)
    address = forms.IntegerField()


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    count = forms.IntegerField(initial=10, min_value=1, max_value=20, required=False)


class VerifycodeValidationForm(forms.Form):
    token = forms.CharField(max_length=64)
    user_name = forms.CharField(min_length=11, max_length=11)
    verify_code = forms.CharField(max_length=6)