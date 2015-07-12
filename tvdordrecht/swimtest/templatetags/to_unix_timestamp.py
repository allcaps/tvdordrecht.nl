# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
register = template.Library()


@register.filter
def to_unix_timestamp(value):
    return 10 #datetime.combine(datetime(1970, 1, 1), value).total_seconds()

