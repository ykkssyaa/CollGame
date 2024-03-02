import os

from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models


def user_photo_path(instance, filename):
    user_id = instance.id
    user_username = instance.username
    _, file_extension = os.path.splitext(filename)
    return f'users/{user_id}_{user_username}{file_extension}'


class User(AbstractUser):
    photo = models.ImageField(upload_to=user_photo_path, blank=True, null=True, verbose_name='photo')
    steam_id = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    games = models.ManyToManyField('games.Game', related_name='games_in_collection', blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/users/{self.username}'


class UserList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    games = models.ManyToManyField('games.Game', related_name='games_in_list', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.user:
            existing_lists = UserList.objects.filter(name=self.name, user=self.user)
            if self.pk:
                existing_lists = existing_lists.exclude(pk=self.pk)
            if existing_lists.exists():
                raise ValidationError('Список с таким именем уже существует для этого пользователя.')
