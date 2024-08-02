from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class CustomUser(AbstractUser):
    username = None
    unique_id = models.CharField(max_length=12, unique=True, default=None)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True)

    USERNAME_FIELD = 'unique_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.unique_id