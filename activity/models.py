from django.db import models
from django.urls import reverse_lazy


class GameDictionary(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('activity:dictionary_page', kwargs={'id': self.id})


class Activity(models.Model):
    dictionary = models.ForeignKey(GameDictionary, on_delete=models.CASCADE)
    hours = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)


class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE)
    stars = models.IntegerField()
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)


class LikeReview(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    value = models.BooleanField(default=True)

