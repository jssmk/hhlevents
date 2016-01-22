from django import template
from django.conf import settings

register = template.Library()

# get value from settings for template display use
@register.simple_tag
def get_settings(name):
    return getattr(settings, name, "")