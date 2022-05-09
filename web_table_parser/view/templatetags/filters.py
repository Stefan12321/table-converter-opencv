from django import template

register = template.Library()


@register.simple_tag(name="range")
def range_(value: int):
    print(list(range(10)))
    return list(range(value))
