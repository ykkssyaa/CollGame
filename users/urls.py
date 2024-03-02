from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

import users.views as views

from . import views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('<str:username>/reviews', views.user_reviews, name='profile_reviews'),
    path('<str:username>/collection', views.UserCollection.as_view(), name='profile_collection'),
    path('<str:username>', views.profile, name='profile'),
]
