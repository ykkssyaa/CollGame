from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

import users.views as views

from . import views

urlpatterns = [
    path('addlist', views.add_list, name='add_list'),
    path('deletelist', views.delete_list, name='delete_list'),
    path('add-to-list', views.add_game_to_list, name='add_to_list'),
    path('lists-with-game/', views.lists_with_game, name='lists_with_game'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('<str:username>/reviews', views.user_reviews, name='profile_reviews'),
    path('<str:username>/collection', views.UserCollection.as_view(), name='profile_collection'),
    path('<str:username>', views.profile, name='profile'),
]
