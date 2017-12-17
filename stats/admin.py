from django.contrib import admin

from .models import Season
from .models import Team, Match, TeamMatch, PlayerMatch, Week
from .models import Player
from .models import TeamPlayer
from .models import Role
from .models import Item
from .models import Champion
from .models import SummonerSpell


class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player Info', {'fields': ['name', 'rank']}),
    ]
    inlines = [TeamPlayerInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamPlayerInline]

class TeamMatchInline(admin.TabularInline):
    model = TeamMatch
    extra = 0

class PlayerMatchInline(admin.TabularInline):
    model = PlayerMatch
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    inlines = [TeamMatchInline, PlayerMatchInline]

class MatchInline(admin.StackedInline):
    model = Match
    extra = 0

class WeekAdmin(admin.ModelAdmin):
    inlines = [MatchInline]


admin.site.register(Role)
admin.site.register(Season)
admin.site.register(Item)
admin.site.register(Champion)
admin.site.register(SummonerSpell)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Week, WeekAdmin)
