# -*- coding:utf-8 -*-
OK = 0

UNKNOWN_ERROR = 1
HTTPS_REQUIRED = 2
PARAM_REQUIRED = 3
DATA_ERROR = 4
DB_ERROR = 5
DB_INTEGRITY_ERROR = 6
DB_NOTEXIST_ERROR = 7
METHOD_ERROR = 8
CODE_INVALID = 9

USER_PWD_ERROR = 10
USER_CANCEL_CONNECT = 11
USER_REGISTERED = 12
USER_CANCEL_REGISTER = 13
USER_NOT_EXIST = 14
USER_LOGIN_FAILED = 15
USER_LOGOUT_FAILED = 16
TOKEN_INVALID = 17
TOKEN_VALIDATION_FAIL = 18
EMAIL_SEND_FAILED = 19

REMOVE_FAILED = 20
ORDER_STATUS_ERROR = 21
PROMOTION_REACH_MAX = 22
DISH_REACH_MAX = 23
ORDER_DISH_REACH_MAX = 24

CODE_MESSAGE = {
    OK: {},
    UNKNOWN_ERROR: {"error_info": u'未知错误'},  # ugettext("Unknown error."),
    HTTPS_REQUIRED: {"error_info": u'请使用HTTPS请求'},  # ugettext("HTTPS required."),
    PARAM_REQUIRED: {"error_info": u'缺少必要参数'},  # ugettext("Parameter required."),
    DATA_ERROR: {"error_info": u'数据错误'},  # ugettext("Data error."),
    DB_ERROR: {"error_info": u'数据库错误'},  # ugettext("Database error."),
    DB_INTEGRITY_ERROR: {"error_info": u'插入重复值或外键不存在'},
    DB_NOTEXIST_ERROR: {"error_info": u'数据库中不存在的该值'},
    METHOD_ERROR: {"error_info": u'请求方法错误'},
    CODE_INVALID: {"error_info": u'验证码失效'},  # ugettext("Verify code invalid."),

    USER_PWD_ERROR: {"error_info": u'用户密码错误'},
    USER_CANCEL_CONNECT: {"error_info": u'用户断开了连接'},  # ugettext("User cancel the connection."),
    USER_REGISTERED: {"error_info": u'用户已经注册'},  # ugettext("User is registered."),
    USER_CANCEL_REGISTER: {"error_info": u'用户放弃了注册'},  # ugettext("User cancel the registration."),
    USER_NOT_EXIST: {"error_info": u'用户不存在'},  # ugettext("User does not exist."),
    USER_LOGIN_FAILED: {"error_info": u'用户名或密码错误'},
    USER_LOGOUT_FAILED: {"error_info": u'用户注销失败'},
    TOKEN_INVALID: {"error_info": u'用户身份认证错误'},  # ugettext("Token invalid."),
    TOKEN_VALIDATION_FAIL: {"error_info": u'用户身份认证失败'},  # ugettext("Token validation fails."),
    EMAIL_SEND_FAILED: {"error_info": u'邮件发送失败'},
    REMOVE_FAILED: {"error_info": u'删除失败'},
    ORDER_STATUS_ERROR: {"error_info": u'订单状态错误'},
    PROMOTION_REACH_MAX: {"error_info": u'促销活动数量超过限制值'},
    DISH_REACH_MAX: {"error_info": u'菜品数量超过限制值'},
    ORDER_DISH_REACH_MAX: {"error_info": u'订单中菜品数量超过限制值'},
    }

