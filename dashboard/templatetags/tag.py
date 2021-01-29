from django import template

register = template.Library()

@register.filter
def to_str1(value1):

    v = value1.split(":")[0]
    print("Str1 --> " + str(v))

    return int(v)

@register.filter
def last_str(value):
    v2 = value.split(":")[1].split("-")[1]
    print("Str2 --> " + str(v2))

    return int(v2)
