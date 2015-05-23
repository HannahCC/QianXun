# -*- coding: UTF-8 -*-
from django.db import models

from QianXun.list.models import School, Canteen
from conf.enum_value import IS_VALID
from conf.default_value import MANAGER_PASSWORD


class SchoolManager(models.Model):
    """
    学校管理员
    """
    school = models.ForeignKey(School, verbose_name=u'学校')
    user_name = models.CharField(u'联系方式', max_length=11, unique=True)
    name = models.CharField(u'姓名', max_length=64)
    token = models.CharField(u'用户认证口令', max_length=64, blank=True)
    password = models.CharField(u'用户密码', max_length=64, default=MANAGER_PASSWORD)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'学校管理员'
        verbose_name_plural = u'学校管理员'
        unique_together = ('school', 'name')

    def __unicode__(self):
        return "-".join([self.school.school_name, self.name])


class CanteenManager(models.Model):
    """
    食堂管理员
    """
    canteen = models.ForeignKey(Canteen, verbose_name=u'食堂')
    user_name = models.CharField(u'联系方式', max_length=11, unique=True)
    name = models.CharField(u'姓名', max_length=64)
    token = models.CharField(u'用户认证口令', max_length=64, blank=True)
    password = models.CharField(u'用户密码', max_length=64, default=MANAGER_PASSWORD)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'食堂管理员'
        verbose_name_plural = u'食堂管理员'
        unique_together = ('canteen', 'name')

    def __unicode__(self):
        return "-".join([self.canteen.school.school_name, self.canteen.canteen_name, self.name])

