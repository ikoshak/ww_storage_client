import os, base64, urllib, urllib2, random

from django.conf import settings


def get_file_path(filename):
    """
    Get file path with file name
    """
    return os.path.join(filename[0], filename[1])


def get_file_url(filename):
    """
    Get file url
    """
    server, file = filename.split('_')
    config = settings.WW_STORAGES_LIST.get(server)
    return '/'.join([config.get('web_url'), get_file_path(file), file])


def put_to_server(file):
    """
    puts file to one of available server. return filename
    """
    content = b''
    for c in file.chunks():
        content += c
    data = {'name': base64.b64encode(file.name), 'content': base64.b64encode(content)}
    server = settings.WW_STORAGES_LIST.get(random.choice(settings.WW_STORAGES_LIST.keys()))

    response = urllib2.urlopen(server.get('upload_url'), urllib.urlencode(data))
    return response.read()
