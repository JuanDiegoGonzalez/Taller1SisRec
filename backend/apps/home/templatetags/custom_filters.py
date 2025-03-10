from django import template

register = template.Library()

@register.filter
def dict_lookup(d, key):
    """ Permite acceder a valores en un diccionario desde un template """
    return d.get(key, None)

@register.filter
def split(value, delimiter=","):
    """ Divide una cadena en una lista usando el delimitador dado """
    return value.split(delimiter)
