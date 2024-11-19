from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django_otp.models import Device

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

class TOTPDevice(Device):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='custom_totpdevices')
    name = models.CharField(max_length=64, unique=True)
    confirmed = models.BooleanField(default=False)