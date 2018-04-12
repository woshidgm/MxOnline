# -*- coding: utf-8 -*-
__author__ = 'dgm'
__date__ = '2018/3/30 19:32'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))  # 装饰器， 用于判断是否登陆，否则跳转至登陆页面
    def dispatch(self, request, *args, **kwargs):      # 必须写 dispatch
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)  # 这种写法只是为了调用那个装饰器