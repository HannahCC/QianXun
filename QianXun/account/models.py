# -*- coding: UTF-8 -*-
from django.db import models

from QianXun.list.models import School, Building, Canteen
from conf.enum_value import IS_VALID, IS_VIP, USER_TYPE, WINDOW_STATUS
from conf.default_value import WINDOW_PASSWORD, CUSTOMER_PASSWORD, GRADE


class Window(models.Model):
    """
    卖家注册
    """
    school = models.ForeignKey(School, verbose_name=u'学校')
    canteen = models.ForeignKey(Canteen, verbose_name=u'食堂')
    user_name = models.CharField(u'联系方式', max_length=11, unique=True)
    token = models.CharField(u'用户认证口令', max_length=64, blank=True)
    client_id = models.CharField(u'用户设备', max_length=64)
    registration_id = models.CharField(u'PushID', max_length=64)
    name = models.CharField(u'法人代表', max_length=64)
    password = models.CharField(u'用户密码', max_length=64, default=WINDOW_PASSWORD)
    version = models.CharField(u'应用版本', max_length=64)
    window_name = models.CharField(u'窗口名称', max_length=64)
    window_status = models.SmallIntegerField(u'窗口状态', choices=WINDOW_STATUS, default=WINDOW_STATUS[0][0])
    img_addr = models.ImageField(u'窗口商标', blank=True, null=True, upload_to=r'windows\%Y\%m\%d', max_length=100)
    sales = models.IntegerField(u'销量', default=0)
    grade = models.FloatField(u'评级', default=GRADE)
    comment_number = models.IntegerField(u'评论数量', default=0)
    promotion_number = models.IntegerField(u'活动数量', default=0)
    deliver_time_number = models.IntegerField(u'配送时间数量', default=0)
    dish_number = models.IntegerField(u'菜品数量', default=0)
    calculate_time = models.DateTimeField(u'上次计算时间', auto_now=True)  # 上次计算窗口销量的时间
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'窗口'
        verbose_name_plural = u'窗口'
        unique_together = ('canteen', 'window_name')

    def __unicode__(self):
        return "-".join([self.canteen.school.school_name, self.canteen.canteen_name, self.window_name])

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Window.objects.get(id=self.id)
            if this.img_addr != self.img_addr:
                this.img_addr.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Window, self).save(*args, **kwargs)


class Customer(models.Model):
    """
    买家注册
    """
    school = models.ForeignKey(School, verbose_name=u'学校')
    user_name = models.CharField(u'联系方式', max_length=11, unique=True)
    token = models.CharField(u'用户认证口令', max_length=64, blank=True)
    client_id = models.CharField(u'用户设备', max_length=64)
    registration_id = models.CharField(u'PushID', max_length=64)
    password = models.CharField(u'用户密码', max_length=64, default=CUSTOMER_PASSWORD)
    user_type = models.SmallIntegerField(u'用户类别', choices=USER_TYPE)
    nick_name = models.CharField(u'用户昵称', max_length=64, blank=True, unique=True)
    version = models.CharField(u'应用版本', max_length=64)
    is_VIP = models.SmallIntegerField(u'是否会员', choices=IS_VIP, default=IS_VIP[0][0])
    VIP_balance = models.IntegerField(u'会员权限剩余次数', default=0)
    VIP_deadline = models.DateField(u'会员权限截止日期', blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])
    building = models.ManyToManyField(Building, verbose_name=u'地址', blank=True, null=True)

    class Meta:
        verbose_name = u'顾客'
        verbose_name_plural = u'顾客'

    def __unicode__(self):
        return "-".join([USER_TYPE[self.user_type-1][1], self.nick_name])


class Address(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=u'顾客')
    addr = models.CharField(u'自定义地址', max_length=64)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'顾客_自定义地址'
        verbose_name_plural = u'顾客_自定义地址'

    def __unicode__(self):
        # return "-".join([self.customer.nick_name, self.addr])
        return self.addr


class VerifyCode(models.Model):
    """
    验证码
    """
    user_name = models.CharField(u'手机号', max_length=11, unique=True)
    verify_code = models.CharField(u'验证码', max_length=6, unique=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)