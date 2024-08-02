import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

temp_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
main_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
