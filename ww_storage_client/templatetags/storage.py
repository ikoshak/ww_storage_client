# encoding: utf-8
from django import template
import core.storage as storage


register = template.Library()


@register.simple_tag(takes_context=True)
def file_url(context, filename, **kwargs):
    return storage.get_file_url(filename)

