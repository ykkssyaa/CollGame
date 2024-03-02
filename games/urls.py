from django.contrib import admin
from django.urls import path

import games.views as views

urlpatterns = [
    path('', views.FindGames.as_view(), name='find_games'),
    path('<slug:game_slug>/add', views.add_game, name='add_game'),
    path('<slug:game_slug>/delete', views.delete_game, name='delete_game'),
    path('<slug:game_slug>', views.game_page, name='game_page'),
]
