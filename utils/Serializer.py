# -*- encoding:utf-8 -*-
__author__ = 'Hannah'
import simplejson
from django.db import models
from django.core.serializers import serialize, deserialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from utils.TimeLocalize import localize_time


class ModelEncoder(simplejson.JSONEncoder):
    """
    继承自simplejson的编码基类，用于处理Queryset或models.Model类型的对象
            如果传入的是Queryset实例
            直接使用Django内置的序列化工具进行序列化
            但是如果直接返回serialize('json',obj),则会多出前后的双引号,在simplejson序列化时会被从当成字符串处理
            因此这里先获得序列化后的对象,然后再用simplejson反序列化一次,得到一个标准的字典（dict）对象

            如果传入的是单个对象，区别于QuerySet的就是
            Django不支持序列化单个对象
            因此，首先用单个对象来构造一个只有一个对象的数组,可以看做是QuerySet对象
            然后此时再用Django来进行序列化,就如同处理QuerySet一样
            但是由于序列化QuerySet会被'[]'所包围,因此使用string[1:-1]来去除'[]'
    """
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return simplejson.loads(serialize('json', obj))
        if isinstance(obj, models.Model):
            return simplejson.loads(serialize('json', [obj])[1:-1])
        return simplejson.JSONEncoder.default(self, obj)


class ObjectEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        if isinstance(obj, list):
            dict_list = []
            for o in obj:
                dict_list.append(o.__dict__)
            return dict_list
        return simplejson.JSONEncoder.default(self, obj)


def __get_json(data):
    """
    基本类型的数据转成JSON格式（QuerySet、models.Model、基本数据类型<可以直接序列表化的>）
    """
    json_data = simplejson.dumps(data, cls=ModelEncoder, encoding='utf8', ensure_ascii=False)
    return json_data


def __get_json_from_model(data):
    """
    如果是查询结果，需要对结果进行一些处理
    将“fields”用“fields”中的“data”字段代替
    若“data”中存在“password”字段，将其去掉
    """
    data = localize_time(data)
    json_data = __get_json(data)
    dict_data = simplejson.loads(json_data)    # convert json-str to a dict
    if 'fields' in dict_data:
        dict_data = dict_data['fields']   # adjust the structure of dict
    if 'password' in dict_data:
        del dict_data['password']
    return dict_data


def __get_json_from_object(data):
    json_data = simplejson.dumps(data, cls=ObjectEncoder, ensure_ascii=False)
    return json_data


def json_response(status, data):
    """
    将结果转换为特定格式的json，作为返回
    """
    json = {}
    json.update({"status": status})
    json.update({"data": data})
    return HttpResponse(__get_json(json), content_type='application/json; charset=utf-8')


def json_response_from_model(status, data, model_id='', extra_data_name='', extra_data=None):
    """
    将属于model.Model类型的data转化为JSON格式，并进行包装，作为返回
    """
    json = {}
    json.update({"status": status})
    json_data = __get_json_from_model(data)
    if model_id:
        json_data.update({'id': model_id})
    if extra_data_name:
        json_data.update({extra_data_name: extra_data})
    json.update({"data": json_data})
    return HttpResponse(__get_json(json), content_type='application/json; charset=utf-8')


def json_response_from_object(status, data, object_name=""):
    """
    将结果转换为特定格式的json，作为返回
    """
    json = {}
    json.update({"status": status})
    json_data = simplejson.loads(__get_json_from_object(data))
    if object_name:
        json_data_dict = {}
        json_data_dict.update({object_name: json_data})
        json.update({"data": json_data_dict})
    else:
        json.update({"data": json_data})
    return HttpResponse(__get_json(json), content_type='application/json; charset=utf-8')


def json_back(json_str):
    """
    进行Json字符串的反序列化
    一般来说，从网络得回的POST（或者GET）参数中所包含json数据
    例如，用POST传过来的参数中有一个key value键值对为
    request.POST['update']= "[{pk:1,name:'changename'},{pk:2,name:'changename2'}]"
    or
    request.POST['update'] = "{pk:1,name:'changename'}"      '[{"dish":1,"number":1},{"dish":2,"number":1}]'

    if json[0] == '[':
        return deserialize('json', json)
    else:
        return deserialize('json', '[' + json + ']')
    """
    return simplejson.loads(json_str)

