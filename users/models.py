from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):

    # role = models.CharField(max_length=50, choices=Role.choices, default = Role.STUDENT)
    email = models.EmailField(unique=True)
    description = models.TextField('Description', max_length=600, default='', blank=True)


    def __str__(self):
        return self.email
