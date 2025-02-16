from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    role = models.CharField(max_length=10, default="USER")

    def __str__(self):
        return self.username