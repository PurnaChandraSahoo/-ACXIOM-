from django import template
register = template.Library()
@register.filter
def getattribute(obj, attr):
    value = getattr(obj, attr, "")
    if callable(value):
        try: value = value()
        except TypeError: return ""
    return value
