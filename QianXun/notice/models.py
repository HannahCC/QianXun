# -*- coding: UTF-8 -*-
from django.db import models

from QianXun.list.models import School, Canteen
from QianXun.manager.models import SchoolManager, CanteenManager
from conf.enum_value import IS_VALID


class SchoolNotice(models.Model):
    """
    学校管理员的发布通知
    """
    manager = models.ForeignKey(SchoolManager, verbose_name=u'作者')
    school = models.ForeignKey(School, verbose_name=u'学校')
    title = models.CharField(u'标题', max_length=64)
    content = models.TextField(u'公告内容')
    read_times = models.IntegerField(u'浏览次数', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'学校公告'
        verbose_name_plural = u'学校公告'

    def __unicode__(self):
        return self.title


class CanteenNotice(models.Model):
    """
    学校管理员的发布通知
    """
    manager = models.ForeignKey(CanteenManager, verbose_name=u'作者')
    canteen = models.ForeignKey(Canteen, verbose_name=u'食堂')
    title = models.CharField(u'标题', max_length=64)
    content = models.TextField(u'公告内容')
    read_times = models.IntegerField(u'浏览次数', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'食堂公告'
        verbose_name_plural = u'食堂公告'

    def __unicode__(self):
        return self.title
