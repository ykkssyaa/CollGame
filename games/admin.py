from django.contrib import admin

from .models import Game, GameStudio, GamesLinks, Platform, Release


class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)


class LinksAdmin(admin.ModelAdmin):
    list_display = ("game", "name", "link")


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("game", "platform", "release_date")


admin.site.register(Game, GameAdmin)
admin.site.register(GameStudio)
admin.site.register(GamesLinks, LinksAdmin)
admin.site.register(Platform)
admin.site.register(Release, ReleaseAdmin)


