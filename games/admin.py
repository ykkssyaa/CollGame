from django.contrib import admin

from .models import Game, GameStudio, GamesLinks, Platform, Release

admin.site.register(Game)
admin.site.register(GameStudio)
admin.site.register(GamesLinks)
admin.site.register(Platform)
admin.site.register(Release)


