# -*- coding: UTF-8 -*-
__author__ = 'Hannah'

IS_VALID = (
    (0, u'否'),
    (1, u'是'),
)

IS_VIP = (
    (0, u'否'),
    (1, u'是'),
)

IS_HEAT = (
    (0, u'常温'),
    (1, u'加热'),
)

FEEDBACK_TYPE = (
    (1, u'用户意见'),
    (2, u'崩溃报告'),
)


USER_TYPE = (
    (1, u'学生'),
    (2, u'教工'),
    (3, u'其他'),
)

WINDOW_STATUS = (
    (1, u'未审核'),
    (2, u'审核通过'),
    (3, u'审核未通过'),
    (4, u'正常营业'),
    (5, u'歇业'),
)

ORDER_STATUS = (
    (11, u'未付款'),
    (21, u'已付款'),
    (31, u'已受理'),
    (32, u'已拒绝'),
    (33, u'已取消'),
    (41, u'配送中'),
    (420, u'已退款'),
    (50, u'待评价'),
    (60, u'已评价'),
)
# 1x => 2x => 3x => 4x => 5x
# x0 : 表示状态已终结，不可再变更

DELIVERY_DATE = (
    (1, u'当天'),
    (2, u'第二天'),
)

LOGINTYPE = (
    (0, u'学校管理员'),
    (1, u"餐厅管理员"),
)

ORDER_BY = (
    (0, u'-sales'),
    (1, u'price'),
    (2, u'-grade'),
)