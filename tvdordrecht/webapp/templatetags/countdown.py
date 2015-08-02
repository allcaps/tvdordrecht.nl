from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def countdown(value):
    days = value - timezone.now.date()
    return days
