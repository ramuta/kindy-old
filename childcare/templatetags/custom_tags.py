from django import template
from utils.deployment import is_local_env

register = template.Library()


@register.simple_tag
def is_not_local():
    return is_local_env()