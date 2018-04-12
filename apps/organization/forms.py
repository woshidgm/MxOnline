# -*- coding: utf-8 -*-
__author__ = 'dgm'
__date__ = '2018/3/27 21:39'
from django import forms
from operation.models import UserAsk
import re
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=5)


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):   # 必须以clean开头 验证mobile字段
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']  # 去除mobile的值
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")