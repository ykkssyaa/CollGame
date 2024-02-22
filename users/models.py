from django.contrib.auth.models import AbstractUser, User
from django.db import models

class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='photo')
    steam_id = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    games = models.ManyToManyField('games.Game', related_name='games_in_collection', blank=True)

    def __str__(self):
        return self.username


class UserList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    games = models.ManyToManyField('games.Game', related_name='games_in_list', blank=True)



