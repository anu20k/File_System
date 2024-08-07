from django.db import models
from django.conf import settings
import os
import mimetypes
import hashlib
from django.utils import timezone


class CATEGORY(models.TextChoices):
    DIABETES = "Diabetes"
    BLOODPRESSURE = "Blood_pressure",
    ASTHMA = "Asthma"
    
    

class Category(models.Model):
    # category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, choices=CATEGORY.choices)
    category_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name

# def upload_to(instance, filename):
#     return os.path.join(instance.directory, filename)

class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    file = models.FileField(upload_to='')
    file_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField(default=0)
    user_id = models.CharField(max_length=12)
    uploaded_on = models.DateTimeField(default=timezone.now)
    crc32 = models.CharField(max_length=8)
    location = models.CharField(max_length=255)
    key = models.IntegerField(default=42)
   
    

    def save(self, *args, **kwargs):
        # Extract file name from the file path
        if self.file:
            self.file = os.path.basename(self.file.name)
            # self.file_type = self.file.file.content_type
            
        super().save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if not self.file_size and self.file:
            self.file_size = self.file.size
        if not self.file_type and self.file:
            self.file_type = os.path.splitext(self.file.name)[1]
        
        if self.file:
           self.file = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

class UserHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

class UploadHistory(models.Model):
    uploaded_by =models.CharField(max_length=100,null=True)
    category =models.CharField(max_length=100,null=True)
    file = models.FileField(upload_to='',null=True)
    file_type = models.CharField(max_length=100,null=True)
    file_size = models.BigIntegerField(default=0,null=True)
    user_id = models.CharField(max_length=12,null=True)
    uploaded_on = models.DateTimeField(default=timezone.now,null=True)
    crc32 = models.CharField(max_length=8,null=True)
    location = models.CharField(max_length=255,null=True)
    
    
    def save(self, *args, **kwargs):
        # Extract file name from the file path
        if self.file:
            self.file = os.path.basename(self.file.name)
            # self.file_type = self.file.file.content_type
            
        super().save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if not self.file_size and self.file:
            self.file_size = self.file.size
        if not self.file_type and self.file:
            self.file_type = os.path.splitext(self.file.name)[1]
        
        if self.file:
           self.file = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
    


class DownloadHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadHistory, on_delete=models.CASCADE)
    download_timestamp = models.DateTimeField(default=timezone.now)
    


        
    
            


    
    
    
 




