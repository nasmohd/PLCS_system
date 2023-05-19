from django import template

register = template.Library()

@register.filter
def get_item(list, i):
    return list[i]