from django.contrib import admin
from django.urls import path

import games.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('games', views.find_games, name='find_games'),
    path('games/<slug:game_slug>', views.game_page, name='game_page'),
]
