from django.contrib import admin

from .models import Game, GameStudio, GamesLinks, Platform, Release


class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)


admin.site.register(Game, GameAdmin)
admin.site.register(GameStudio)
admin.site.register(GamesLinks)
admin.site.register(Platform)
admin.site.register(Release)


