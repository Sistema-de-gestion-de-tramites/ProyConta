from django import template

register = template.Library()

@register.simple_tag
def get_verbose_name(object, fieldnm):
    return object._meta.get_field(fieldnm).verbose_name

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural