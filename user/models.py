from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.username








