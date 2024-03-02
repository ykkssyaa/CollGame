import os

from django.db import models
from pytils.translit import slugify
from taggit.managers import TaggableManager


def game_poster_path(instance, filename):
    game_slug = instance.slug
    _, file_extension = os.path.splitext(filename)
    return f'posters/{game_slug}{file_extension}'


class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    studio = models.ForeignKey('GameStudio', on_delete=models.PROTECT, null=True)

    poster = models.ImageField(upload_to=game_poster_path, null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/games/{self.slug}'


class GameStudio(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Release(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    release_date = models.DateField()


class GamesLinks(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=" ")
    link = models.URLField()
