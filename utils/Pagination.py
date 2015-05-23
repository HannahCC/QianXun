__author__ = 'Hannah'
from conf.default_value import PAGE, COUNT


def get_paginator(pagination_dict):
    paginator = []
    page = PAGE
    count = COUNT
    if pagination_dict['page']:
        page = pagination_dict['page']
    if pagination_dict['count']:
        count = pagination_dict['count']
    start = (page-1)*count
    end = start+count
    paginator.append(start)
    paginator.append(end)
    return paginator

