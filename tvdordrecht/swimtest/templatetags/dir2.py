from django import template
register = template.Library()


@register.filter
def dir2(value):
    return dir(value)