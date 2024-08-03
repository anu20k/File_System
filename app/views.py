

from operator import xor

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import UploadedFileForm
from .models import UploadedFile,UploadHistory
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse, Http404
import os
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import mimetypes
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

import os
from django.conf import settings
import mimetypes
from .forms import UploadedFileForm
from django.contrib.auth.decorators import login_required
import zlib

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .storage import temp_storage, main_storage 
from django.core.files.storage import default_storage as main_storage
from django.core.files.storage import default_storage as temp_storage
from .utils import get_directory_structure

from django.shortcuts import render
from django.conf import settings
from .utils import get_directory_structure

from django.shortcuts import render
from django.conf import settings
from .utils import get_directory_structure
import os
from django.core.files.base import ContentFile

import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.parse import unquote

def file_explorer(request):
    rootdir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    directory_structure = get_directory_structure(rootdir)
    return render(request, 'app/file_explorer.html', {
        'structure': directory_structure,
        'MEDIA_URL': settings.MEDIA_URL,
    })






def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def xor_encrypt_decrypt(data, key):
    # XOR each byte with the key
    return bytearray([b ^ key for b in data])







# def view_file(request, file_path):
#     # Construct the full file path
#     file_path = os.path.join(settings.MEDIA_ROOT, unquote(file_path))
#     print(f"Resolved file path: {file_path}")
    
#     # Determine the file's MIME type
#     mime_type, _ = mimetypes.guess_type(file_path)
#     if mime_type is None:
#         mime_type = 'application/octet-stream'
     
    
#     try:
#         # Read the encrypted file
#         with open(file_path, 'rb') as f:
#             file_name = f.read()
        
        
        

#         # Prepare the HTTP response with decrypted data
#         response = HttpResponse(file_name, content_type=mime_type)
#         response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
#         return response
    
#     except Exception as e:
#         return HttpResponse(f"Error reading or decrypting file: {e}", status=500)


def save_file_in_chunks(uploaded_file, storage, path):
    with storage.open(path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return storage.path(path)

def calculate_crc32_from_chunks(file_path):
    crc32 = 0
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            crc32 = zlib.crc32(chunk, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def encrypt_file_in_chunks(file_path, key):
    encrypted_data = bytearray()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            encrypted_data.extend(xor_encrypt_decrypt(chunk, key))
    return bytes(encrypted_data)

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')

        if form.is_valid():
            for uploaded_file in files:
                # Step 1: Save the file to temporary storage
                temp_file_path = save_file_in_chunks(uploaded_file, temp_storage, uploaded_file.name)
                temp_file_full_path = temp_storage.path(temp_file_path)

                # Step 2: Calculate CRC32 checksum
                crc32_checksum = calculate_crc32_from_chunks(temp_file_full_path)

                # Step 3: Check if the CRC32 checksum already exists in the database
                if UploadedFile.objects.filter(crc32=crc32_checksum).exists():
                    # File with the same CRC32 checksum already exists
                    temp_storage.delete(temp_file_path)
                    messages.error(request, f'File with the same content already exists: {uploaded_file.name}')
                else:
                    # Step 4: Encrypt the file data
                    key = 42  # Simple key for XOR encryption, use a more secure method in production
                    encrypted_data = encrypt_file_in_chunks(temp_file_full_path, key)

                    # Step 5: Construct the dynamic path
                    user_id = form.cleaned_data['user_id']
                    year = form.cleaned_data['uploaded_on'].year
                    category = form.cleaned_data.get('category')  # Assuming category is a foreign key, adjust as needed
                    file_name = uploaded_file.name

                    dynamic_path = f'uploads/{user_id}/{year}/{category}/{file_name}'
                    main_file_path = main_storage.path(dynamic_path)

                    print(main_file_path)
                    # Check if a file with the same name exists for the user
                    existing_file = UploadedFile.objects.filter(
                        uploaded_by=request.user,
                        category=category,
                        user_id=user_id,
                        file=file_name
                       
                        
                    ).first()

                    if existing_file:
                        # If file with the same name exists, check if the checksum is different
                        if existing_file.crc32 != crc32_checksum:
                            # Replace the existing file with the new file
                            main_storage.delete(main_file_path)  # Delete the existing file
                            main_storage.save(dynamic_path, ContentFile(encrypted_data))  # Save the new encrypted file

                            # Update the model
                            existing_file.crc32 = crc32_checksum
                            existing_file.key = key  # Save the encryption key
                            existing_file.save()

                            messages.success(request, f'File replaced successfully: {uploaded_file.name}')
                        else:
                            # File with the same content already exists
                            temp_storage.delete(temp_file_path)
                            messages.error(request, f'File with the same content already exists: {uploaded_file.name}')
                    else:
                        # Move the file to the main storage
                        main_storage.save(dynamic_path, ContentFile(encrypted_data))

                        # Save the new file details in the database
                        new_file = UploadedFile(
                            uploaded_by=request.user,
                            category=category,
                            file=dynamic_path,
                            user_id=user_id,
                            uploaded_on=form.cleaned_data['uploaded_on'],
                            crc32=crc32_checksum,
                           
                        )
                        new_file.save()

                        # new_history=UploadHistory(
                        #     uploaded_by=request.user,
                        #     category=category,
                        #     file=dynamic_path,
                        #     user_id=user_id,
                        #     uploaded_on=form.cleaned_data['uploaded_on'],
                        #     crc32=crc32_checksum,
                        #     )
                        # new_history.save(using='history')
                        
                        # print(main_file_path)
                        messages.success(request, f'File uploaded successfully: {uploaded_file.name}')

                    # Delete the temporary file
                    temp_storage.delete(temp_file_path)

            return redirect('upload_file')  # Replace with your actual success URL
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
    else:
        form = UploadedFileForm()
    return render(request, 'app/upload_file.html', {'form': form})



def decrypt_file_in_chunks(file_path, key):
    decrypted_data = bytearray()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            decrypted_data.extend(xor_encrypt_decrypt(chunk, key))
    return bytes(decrypted_data)

def decrypt_file(request, file_path):
    file_path = file_path.lstrip('/')
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    logger.debug(f"Full file path: {full_file_path}")
    
    if not os.path.isfile(full_file_path):
        logger.error(f"File not found: {full_file_path}")
        return HttpResponse("File not found.", status=404)

    key = 42  # Should be the same key used for encryption
    decrypted_data = decrypt_file_in_chunks(full_file_path, key)
    
    # Determine the file content type
    content_type = 'application/octet-stream'
    if full_file_path.endswith('.pdf'):
        content_type = 'application/pdf'
    elif full_file_path.endswith('.txt'):
        content_type = 'text/plain'
    elif full_file_path.endswith('.jpg') or full_file_path.endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif full_file_path.endswith('.png'):
        content_type = 'image/png'

    response = HttpResponse(decrypted_data, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
    return response