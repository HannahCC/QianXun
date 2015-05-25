# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from django import forms
from QianXun.notice.models import CanteenNotice


class NoticeDetailDisplayForm(forms.Form):
    token = forms.CharField(max_length=64)
    notice = forms.IntegerField()


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)


class ChangeNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(ChangeNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CanteenNotice
        fields = ['title', 'content', 'is_valid']


class CreateNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(CreateNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CanteenNotice
        fields = ['title', 'content', 'is_valid']
