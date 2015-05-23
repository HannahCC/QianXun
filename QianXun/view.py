__author__ = 'Hannah'
from django.shortcuts import render_to_response

from utils.Decorator import post_required, exception_handled
from utils.Serializer import _json_response, _json_response_from_model
from account.forms import *
from QianXun.account.db import window
from conf.resp_code import *


def test(request):
    return render_to_response("test/testWindow.html")

@exception_handled
@post_required
def window_register(request):
    window_form = WindowForm()
    print request.method
    if request.method == 'GET':
        return render_to_response('test/testWindow.html', {'form': window_form})
    window_form = WindowForm(request.POST)
    if window_form.is_valid():
        my_window = window.create(window_form)
        return _json_response_from_model(OK, my_window)
    else:
        return _json_response(PARAM_REQUIRED, window_form.errors)