import os, base64, urllib, urllib2, random, json

from django.conf import settings


def get_file_path(filename):
    """
    Get file path with file name
    """
    return os.path.join(filename[0], filename[1])


def get_file_url(filename, thumb=None):
    """
    Get file url
    """
    server, file = filename.split('_')
    config = settings.WW_STORAGES_LIST.get(server)
    if thumb:
        real_file = thumb+'@'+file
    else:
        real_file = file
    return '/'.join([config.get('web_url'), get_file_path(file), real_file])


def put_content_to_server(filename, content):
    """
    puts file content to one of available server. return filename
    """
    data = {'name': base64.b64encode(filename.encode('utf-8')), 'content': base64.b64encode(content)}
    server = settings.WW_STORAGES_LIST.get(random.choice(settings.WW_STORAGES_LIST.keys()))

    response = urllib2.urlopen(server.get('upload_url'), urllib.urlencode(data))
    return response.read()


def put_to_server(file):
    """
    puts file to one of available server. return filename
    """
    content = b''
    for c in file.chunks():
        content += c
    data = {'name': base64.b64encode(file.name.encode('utf-8')), 'content': base64.b64encode(content)}
    server = settings.WW_STORAGES_LIST.get(random.choice(settings.WW_STORAGES_LIST.keys()))

    response = urllib2.urlopen(server.get('upload_url'), urllib.urlencode(data))
    return response.read()


def document_to_pictures(filename):
    """
    send command to storage to generate pictures from document
    """
    server, file = filename.split('_')
    config = settings.WW_STORAGES_LIST.get(server)
    data = {'name': base64.b64encode(file)}
    response = urllib2.urlopen(config.get('document_to_picture_url'), urllib.urlencode(data))
    return json.loads(response.read())


def get_document_content(filename, file_format):
    """
    send command to storage to get document content
    """
    server, file = filename.split('_')
    config = settings.WW_STORAGES_LIST.get(server)
    data = {'name': base64.b64encode(file), 'format': file_format}
    response = urllib2.urlopen(config.get('get_document_content_url'), urllib.urlencode(data))
    result = json.loads(response.read())
    return result['content']
