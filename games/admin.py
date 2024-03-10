from django.contrib import admin
from django.utils.html import format_html

from .models import Game, GameStudio, GamesLinks, Platform, Release


class GamesLinksInline(admin.TabularInline):
    model = GamesLinks
    extra = 1


class ReleaseInline(admin.TabularInline):
    model = Release
    extra = 1


class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "poster_display", "studio_name", "tags_display")
    inlines = [GamesLinksInline, ReleaseInline]

    def studio_name(self, obj):
        return obj.studio.name if obj.studio else ""
    studio_name.short_description = "Studio"

    def poster_display(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.poster.url)
        else:
            return ""
    poster_display.short_description = "Poster"

    def tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_display.short_description = "Tags"


class LinksAdmin(admin.ModelAdmin):
    list_display = ("game", "name", "link")


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("game", "platform", "release_date")


admin.site.register(Game, GameAdmin)
admin.site.register(GameStudio)
admin.site.register(Platform)
admin.site.register(GamesLinks, LinksAdmin)
admin.site.register(Release, ReleaseAdmin)


