__author__ = 'Hannah'
from conf.default_value import PAGE, COUNT


def get_paginator(pagination_dict):
    paginator = []
    page = pagination_dict.get('page', PAGE)
    count = pagination_dict.get('count', COUNT)
    start = (page-1)*count
    end = start+count
    paginator.append(start)
    paginator.append(end)
    return paginator

