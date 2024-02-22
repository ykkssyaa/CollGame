from django.contrib import admin
from django.urls import path

import games.views as views

urlpatterns = [
    path('', views.index, name='index'),
]