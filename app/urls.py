from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_file, file_explorer,decrypt_file
from . import views
from .views import upload_history_report,user_history_report

urlpatterns = [
    path('upload-file/', upload_file, name='upload_file'),
    path('file-explorer/', file_explorer, name='file_explorer'),
    path('decrypt-file/<path:file_path>/', decrypt_file, name='decrypt_file'),
    path('upload-history-report/', upload_history_report, name='upload_history_report'),
    path('user_history_report/', user_history_report, name='user_history_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
