from django.template.defaultfilters import register
from django import template

register = template.Library()

@register.simple_tag
def dict_nested_lookup(dict, k1, k2):
    return dict.get(k1).get(k2)