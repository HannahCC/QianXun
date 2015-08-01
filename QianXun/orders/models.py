# -*- coding: UTF-8 -*-
from django.db import models

from QianXun.account.models import Customer, Window, Address
from QianXun.list.models import Building, PromotionType
from conf.enum_value import IS_VALID, IS_HEAT, ORDER_STATUS, DELIVERY_DATE
from conf.default_value import DELIVERY_COST, GRADE


class DeliverTime(models.Model):
    """
    卖家添加可以订单送达的时间
    """
    window = models.ForeignKey(Window, verbose_name=u'窗口')
    date = models.SmallIntegerField(u'配送日期', choices=DELIVERY_DATE)
    time = models.TimeField(u'配送时间', blank=True, null=True)  # 为空表示尽快到达
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'配送时间'
        verbose_name_plural = u'配送时间'

    def __unicode__(self):
        if self.time:
            time_str = " ".join([DELIVERY_DATE[self.date-1][1], str(self.time)])
        else:
            time_str = " ".join([DELIVERY_DATE[self.date-1][1], u'尽快配送'])
        return time_str
    '''
    def show_datetime(self):
        if self.time:
            time_str = " ".join([DELIVERY_DATE[self.date-1][1], str(self.time)])
        else:
            time_str = " ".join([DELIVERY_DATE[self.date-1][1], u'尽快配送'])
        return time_str
    '''
    def show_time(self):
        if not self.time:
            return u'尽快配送'
        else:
            return self.time
    show_time.short_description = u'配送时间'


class Promotions(models.Model):
    """
    卖家添加促销活动
    """
    window = models.ForeignKey(Window, verbose_name=u'窗口')
    pro_type = models.ForeignKey(PromotionType, verbose_name=u'活动类别')
    rules = models.CharField(u'活动规则', max_length=64)  # 形如满10减2,与活动名称要相符
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'促销活动'
        verbose_name_plural = u'促销活动'

    def __unicode__(self):
        return self.rules


class Dish(models.Model):
    """
    卖家添加菜品
    """
    window = models.ForeignKey(Window, verbose_name=u'窗口')
    dish_name = models.CharField(u'菜品名称', max_length=64)
    price = models.FloatField(u'价格')
    is_heat = models.SmallIntegerField(u'是否加热', choices=IS_HEAT, default=IS_HEAT[0][0])
    description = models.CharField(u'描述', max_length=64, blank=True)
    img_addr = models.ImageField(u'菜品图片', blank=True, null=True,  upload_to=r'dishes\%Y\%m\%d', max_length=100)
    sales = models.IntegerField(u'销量', default=0)
    grade = models.FloatField(u'评级', default=GRADE)
    comment_number = models.IntegerField(u'评论数量', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    calculate_time = models.DateTimeField(u'上次计算时间', auto_now=True)  # 上次计算菜品评级、评论数量的时间
    is_valid = models.SmallIntegerField(u'是否有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'菜品'
        verbose_name_plural = u'菜品'
        ordering = ['dish_name']

    def __unicode__(self):
        return self.dish_name

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Dish.objects.get(id=self.id)
            if this.img_addr != self.img_addr:
                this.img_addr.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super(Dish, self).save(*args, **kwargs)


class Orders(models.Model):
    """
    买家生成订单
    """
    order_id = models.CharField(u'订单号', max_length=64, unique=True)  # window_id , timestamp, random number
    customer = models.ForeignKey(Customer, verbose_name=u'顾客')
    window = models.ForeignKey(Window, verbose_name=u'窗口')
    # this should be a building of the customer
    building = models.ForeignKey(Building, verbose_name=u'楼栋', blank=True, null=True)
    # this should be a address of the customer
    address = models.ForeignKey(Address, verbose_name=u'自定义地址', blank=True, null=True)
    # this should be a time of the window
    deliver_time = models.ForeignKey(DeliverTime, verbose_name=u'送达时间', blank=True, null=True)

    notes = models.CharField(u'备注', max_length=64, default='', blank=True)
    promotion_list = models.CharField(u'优惠活动', max_length=1024, blank=True)
    discount = models.FloatField(u'折扣', default=0)
    food_cost = models.FloatField(u'金额')
    deliver_cost = models.FloatField(u'配送费', default=DELIVERY_COST)
    order_status = models.SmallIntegerField(u'订单状态', choices=ORDER_STATUS, default=ORDER_STATUS[0][0])
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    deal_time = models.DateTimeField(u'成交时间', blank=True, null=True)
    is_valid2customer = models.SmallIntegerField(u'买家有效', choices=IS_VALID, default=IS_VALID[1][0])
    is_valid2window = models.SmallIntegerField(u'卖家有效', choices=IS_VALID, default=IS_VALID[1][0])

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = u'订单'

    def __unicode__(self):
        return "-".join([self.customer.nick_name, self.customer.user_name])

    def show_dishes(self):
        dishes = self.ordersdishes_set.all()
        if dishes:
            dishes_str = ""
            for dish in dishes:
                dishes_str = ",".join([dish.__unicode__(), dishes_str])
            return dishes_str
        else:
            return u"该订单没有菜品"
    show_dishes.short_description = u'菜品'


class OrdersDishes(models.Model):
    """
    订单包含菜品
    """
    orders = models.ForeignKey(Orders, verbose_name=u'订单')
    dish = models.ForeignKey(Dish, verbose_name=u'菜品')
    number = models.IntegerField(u'份数')
    grade = models.FloatField(u'评分', blank=True, null=True)
    text = models.CharField(u'评价', max_length=64, blank=True)
    comment_time = models.DateTimeField(u'评价时间', blank=True, null=True)
    reply = models.CharField(u'回复', max_length=64, blank=True)
    reply_time = models.DateTimeField(u'回复时间', blank=True, null=True)

    class Meta:
        verbose_name = u'订单-菜品'
        verbose_name_plural = u'订单-菜品'

    def __unicode__(self):
        return "-".join([self.dish.dish_name, str(self.number)+u"份"])

