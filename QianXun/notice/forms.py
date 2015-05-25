# -*- coding:utf-8 -*-
__author__ = 'Hannah'

from django import forms
from QianXun.notice.models import CanteenNotice, SchoolNotice


class NoticeDetailDisplayForm(forms.Form):
    token = forms.CharField(max_length=64)
    notice = forms.IntegerField()


class PaginationForm(forms.Form):
    token = forms.CharField(max_length=64)
    page = forms.IntegerField(initial=1, required=False)
    count = forms.IntegerField(initial=10, max_value=20, required=False)


class ChangeCNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(ChangeCNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CanteenNotice
        fields = ['title', 'content', 'is_valid']


class CreateCNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(CreateCNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CanteenNotice
        fields = ['title', 'content', 'is_valid']

class ChangeSNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(ChangeSNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SchoolNotice
        fields = ['title', 'content', 'is_valid']


class CreateSNoticeForm(forms.ModelForm):
    token = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super(CreateSNoticeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SchoolNotice
        fields = ['title', 'content', 'is_valid']

