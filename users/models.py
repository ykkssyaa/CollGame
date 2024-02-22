from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='photo')
    steam_id = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)


