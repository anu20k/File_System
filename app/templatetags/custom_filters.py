from django import template
from django.conf import settings
import urllib.parse

register = template.Library()

@register.filter
def ends_with(value, arg):
    return value.endswith(arg)

@register.filter
def unquote(value):
    return urllib.parse.unquote(value)

@register.filter(name='file_icon')
def file_icon(filename):
    if filename.lower().endswith('.pdf'):
        return 'fas fa-file-pdf'
    elif filename.lower().endswith('.docx'):
        return 'fas fa-file-word'
    elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        return 'fas fa-file-image'
    elif filename.lower().endswith('.png'):
        return 'fas fa-file-image'
    else:
        return 'fas fa-file'
    
@register.filter
def file_path_to_url(file_path):
    return file_path.lstrip('/').replace('/', settings.MEDIA_URL[1:])

