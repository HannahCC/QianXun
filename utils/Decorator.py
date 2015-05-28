__author__ = 'Hannah'

import sys
import logging
import traceback

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from utils.Serializer import json_response
from conf.resp_code import *
from conf.default_value import TOKEN
from QianXun.account.db import window, customer
from QianXun.manager.db import manager


_LOGGER = logging.getLogger(__name__)


def exception_handled(func):
    def _view1(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An ObjectDoesNotExist error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.warning(exception_message)
            return json_response(DB_NOTEXIST_ERROR, CODE_MESSAGE.get(DB_NOTEXIST_ERROR))
        except IntegrityError:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An IntegrityError error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.warning(exception_message)
            return json_response(DB_INTEGRITY_ERROR, CODE_MESSAGE.get(DB_INTEGRITY_ERROR))
        except Exception:
            exc_type, value, tb = sys.exc_info()
            formatted_tb = traceback.format_tb(tb)
            exception_message = 'An error occurred %s: %s traceback=%s' % (exc_type, value, formatted_tb)
            _LOGGER.error(exception_message)
            return json_response(UNKNOWN_ERROR, CODE_MESSAGE.get(UNKNOWN_ERROR))
    return _view1


def post_required(func):
    def _view2(request, *args, **kwargs):
        if request.method != 'POST':
            _LOGGER.info('Post menthod required')
            return json_response(METHOD_ERROR, CODE_MESSAGE.get(METHOD_ERROR))
        return func(request, *args, **kwargs)
    return _view2


def token_required(func):
    def _view(request, *args, **kwargs):
        post = request.POST
        if not post or not post.get('token'):
            _LOGGER.info('Token Required for User')
            return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
        token = post.get('token')
        if token == TOKEN:
            _LOGGER.info('Token is equal to Default TOKEN.')
            return func(request, *args, **kwargs)
        else:
            _LOGGER.info('Token is not equal to Default TOKEN.')
            return json_response(TOKEN_INVALID, CODE_MESSAGE.get(TOKEN_INVALID))
    return _view


def customer_token_required(func):
    def _view(request, *args, **kwargs):
        post = request.POST
        if not post or not post.get('token'):
            _LOGGER.info('Token Required for Customer User')
            return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
        token = post.get('token')
        try:
            my_customer = customer.get_by_token(token)
            _LOGGER.info('Token hit in db for Customer User')
            user_meta = {}
            user_meta.update({'customer_model': my_customer})
            request.user_meta = user_meta
        except ObjectDoesNotExist:
            _LOGGER.info('Token not in db for Customer User.')
            return json_response(TOKEN_INVALID, CODE_MESSAGE.get(TOKEN_INVALID))
        return func(request, *args, **kwargs)
    return _view


def window_token_required(func):
    def _view3(request, *args, **kwargs):
        post = request.POST
        if not post or not post.get('token'):
            _LOGGER.info('Token Required for Window User.')
            return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
        token = post.get('token')
        try:
            my_window = window.get_by_token(token)
            _LOGGER.info('Token hit in db for Window User')
            user_meta = {}
            user_meta.update({'window_model': my_window})
            request.user_meta = user_meta
        except ObjectDoesNotExist:
            _LOGGER.info('Token not in db for Window User.')
            return json_response(TOKEN_INVALID, CODE_MESSAGE.get(TOKEN_INVALID))
        return func(request, *args, **kwargs)
    return _view3


def school_manager_token_required(func):
    def _view3(request, *args, **kwargs):
        post = request.POST
        if not post or not post.get('token'):
            _LOGGER.info('Token Required for School Manager.')
            return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
        token = post.get('token')
        try:
            my_manager = manager.school_get_by_token(token)
            _LOGGER.info('Token hit in db for School Manager')
            user_meta = {}
            user_meta.update({'manager_model': my_manager})
            request.user_meta = user_meta
        except ObjectDoesNotExist:
            _LOGGER.info('Token not in db for School Manager.')
            return json_response(TOKEN_INVALID, CODE_MESSAGE.get(TOKEN_INVALID))
        return func(request, *args, **kwargs)
    return _view3


def canteen_manager_token_required(func):
    def _view3(request, *args, **kwargs):
        post = request.POST
        if not post or not post.get('token'):
            _LOGGER.info('Token Required for Canteen Manager.')
            return json_response(PARAM_REQUIRED, CODE_MESSAGE.get(PARAM_REQUIRED))
        token = post.get('token')
        try:
            my_manager = manager.canteen_get_by_token(token)
            _LOGGER.info('Token hit in db for Manager User')
            user_meta = {}
            user_meta.update({'manager_model': my_manager})
            request.user_meta = user_meta
        except ObjectDoesNotExist:
            _LOGGER.info('Token not in db for Canteen Manager.')
            return json_response(TOKEN_INVALID, CODE_MESSAGE.get(TOKEN_INVALID))
        return func(request, *args, **kwargs)
    return _view3