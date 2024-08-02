from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_file, file_explorer,view_file
from . import views

urlpatterns = [
    path('upload-file/', upload_file, name='upload_file'),
    path('file-explorer/', file_explorer, name='file_explorer'),
   path('view_file/<path:file_path>/', views.view_file, name='view_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
