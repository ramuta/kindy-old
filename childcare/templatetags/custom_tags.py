import os
from django import template

register = template.Library()


@register.tag
def is_local():
    try:
        LOCAL_ENV = os.environ["DJANGO_LOCAL_DEV"]
        if LOCAL_ENV == 0 or LOCAL_ENV == '0':
            return False
        else:
            return True
    except KeyError:
        return True