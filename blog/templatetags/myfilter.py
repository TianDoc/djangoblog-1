# -*- coding: utf-8 -*-
import markdown2
from django import template
from django.template.defaultfilters import stringfilter

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
@stringfilter
def my_rep(value):
    try:
        arr = value.split('-')
        tostr = str(arr[0])+'年 '+str(arr[1])+'月'
    except Exception as e:
        tostr = value
    return tostr

@register.filter
@stringfilter
def my_bj(value):
    try:
        leng = len(str(value))
        if leng == 1:
            tostr = '0'+str(value)+'日'
        else:
            tostr = str(value)+'日'
    except Exception as e:
        tostr = str(value)+'日'
    return tostr

@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown2.markdown(force_text(value),extras=["fenced-code-blocks", "cuddled-lists", "metadata", "tables","spoiler"]))
