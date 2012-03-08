import re
from django import template

register = template.Library()


@register.filter
def placeholders(url):
    return re.findall('\{\s*(\w+)\s*\}', url)


@register.filter
def summary(obj):

    def remove_meta(obj):
        result = obj
        if type(obj) == dict:
            result = {}
            for key, value in obj.items():
                if not key.startswith('special_'):
                    result[key] = remove_meta(value)
        if type(obj) == list:
            result = []
            for value in obj:
                result.append(remove_meta(value))
        return result

    return remove_meta(obj)
