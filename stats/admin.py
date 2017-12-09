from django.contrib import admin

from .models import Team
from .models import Player

class PlayerInLine(admin.TabularInLine):
    model = Player
    extra = 5

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player Info', {'fields': ['summoner_name', 'rank']}),
        ('Team Info',   {'fields': ['team', 'role']}),
    }

class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInLine]

admin.site.register(Player)
admin.site.register(Player, PlayerAdmin)
