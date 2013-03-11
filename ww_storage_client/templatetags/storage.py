# encoding: utf-8
from django import template
import ww_storage_client.storage as storage



register = template.Library()


@register.simple_tag(takes_context=True)
def file_url(context, filename, **kwargs):
    if not filename:
        return kwargs.get('default', '')
    if kwargs.get('thumb'):
        pass

    return storage.get_file_url(filename)

