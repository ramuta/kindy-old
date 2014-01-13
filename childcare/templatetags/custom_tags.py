from django import template
from utils.custom_template_tags import condition_tag

register = template.Library()

@register.tag
@condition_tag
def if_local(object):
    return True