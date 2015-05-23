# -*- coding: UTF-8 -*-
from django.db import models

from conf.enum_value import IS_VALID


class PromotionType(models.Model):
    """
    超级管理员添加促销活动类型(admin中操作)
    """
    pro_type_name = models.CharField(u'活动类别名称', max_length=64, unique=True)
    img_addr = models.ImageField(u'活动图片', upload_to=r'promotions\%Y\%m\%d', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'活动类别'
        verbose_name_plural = u'活动类别'
        ordering = ['update_time']

    def __unicode__(self):
        return self.pro_type_name


class School(models.Model):
    """
    超级管理员要添加学校(admin中操作)
    """
    school_name = models.CharField(u'学校', max_length=64, unique=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'学校'
        verbose_name_plural = u'学校'
        ordering = ['school_name']

    def __unicode__(self):
        return self.school_name


class District(models.Model):
    """
    超级管理员要添加学校对应的校区(admin中操作)
    """
    school = models.ForeignKey(School, verbose_name=u'学校')
    district_name = models.CharField(u'校区', max_length=64)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'校区'
        verbose_name_plural = u'校区'
        unique_together = ('school', 'district_name')
        ordering = ['district_name']

    def __unicode__(self):
        return "-".join([self.school.school_name, self.district_name])


class Building(models.Model):
    """
    超级管理员要添加校区对应的楼栋(admin中操作)
    """
    district = models.ForeignKey(District, verbose_name=u'校区')
    building_name = models.CharField(u'楼栋', max_length=64)
    terminal_id = models.CharField(u'终端机', max_length=64, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'楼栋'
        verbose_name_plural = u'楼栋'
        unique_together = ('district', 'building_name')
        ordering = ['building_name']

    def __unicode__(self):
        return "-".join([self.district.school.school_name, self.district.district_name, self.building_name])


class Canteen(models.Model):
    """
    超级管理员要添加学校对应的食堂(admin中操作)
    """
    school = models.ForeignKey(School, verbose_name=u'学a校')
    canteen_name = models.CharField(u'食堂', max_length=64)
    img_addr = models.ImageField(u'食堂商标', blank=True, null=True, upload_to=r'canteens\%Y\%m\%d', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=1)

    class Meta:
        verbose_name = u'食堂'
        verbose_name_plural = u'食堂'
        unique_together = ('school', 'canteen_name')
        ordering = ['canteen_name']

    def __unicode__(self):
        return "-".join([self.school.school_name, self.canteen_name])


