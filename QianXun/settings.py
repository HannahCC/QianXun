"""
Django settings for QianXun project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^6!y)#4lk(6vl$)gw(6gj^ud#vyhp(a@5wx*%*q%g3t=mmvt6u'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'QianXun.list',
    'QianXun.manager',
    'QianXun.notice',
    'QianXun.account',
    'QianXun.orders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'QianXun.urls'

WSGI_APPLICATION = 'QianXun.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'qianxun',
        'USER': 'root',
        'PASSWORD': 'qianxun123456',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "QianXun/static")
TEMPLATE_URL = '/qianxun/template/'
TEMPLATE_ROOT = os.path.join(BASE_DIR, "QianXun/templates")
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'QianXun/templates'),
)

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static"),
)

# email config
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xiaoyuanbiandang@126.com'
EMAIL_HOST_PASSWORD = 'amvmqidlozssiang'
EMAIL_SUBJECT_PREFIX = '[QianXun_Server]'
EMAIL_USE_TLS = True

SERVER_EMAIL = 'xiaoyuanbiandang@126.com'  # server error will send from here

ADMINS = (
    ('LiChen', 'whulichen@163.com'),     # server error will send to here
)

ADMIN_EMAIL = {
    'APP_DEVELPOER_EMAIL': ['whulichen@163.com'],  # app crash report will send to here
    'MANAGER_EMAIL': ['whulichen@163.com'],  # users feedback will send to here
}

SEND_BROKEN_LINK_EMAILS = True         # set link interrupted warning

# media config
MEDIA_ROOT = r'D:\QianXun\Data\Img'
MEDIA_URL = r'/qianxun/img/'

# version
SERVICE_VERSION = 1
# LOG
LOGGING_STATIC = os.path.join(BASE_DIR,  'logs/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_STATIC+'/', 'all.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_STATIC+'/', 'request.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'warning_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_STATIC+'/', 'warning.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scripts_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_STATIC+'/', 'script.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'third_party_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_STATIC+'/', 'third_party.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'scripts': {
            'handlers': ['scripts_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False
        },
        'utils.Decorator': {
            'handlers': ['default', 'warning_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False
        },
        'utils.Push': {
            'handlers': ['third_party_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False
        },
        'utils.SendMsg': {
            'handlers': ['third_party_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False
        },
        'orders.management.commands.regular_task': {
            'handlers': ['scripts_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False
        },
        'django': {
            'handlers': ['default', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler', 'console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}