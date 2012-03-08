import re
from django import template

register = template.Library()


@register.filter
def placeholders(url):
    return re.findall('\{\s*(\w+)\s*\}', url)
