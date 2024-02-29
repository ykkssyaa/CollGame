from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

import users.views as views

from . import views

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
]
