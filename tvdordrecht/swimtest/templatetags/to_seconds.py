# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def to_seconds(value):
    """
    To seconds
    For time object to seconds.
    """
    seconds = 0
    seconds += value.hour * 3600
    seconds += value.minute * 60
    seconds += value.second
    return seconds