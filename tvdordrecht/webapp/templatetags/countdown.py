from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def countdown(value):
    days = (value - timezone.now().date()).days - 1
    if days == 1:
        return 'Morgen is de grote dag!'
    else:
        return "Nog %d nachtjes slapen..." % days
