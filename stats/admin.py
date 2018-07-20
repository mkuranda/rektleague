from django.contrib import admin

from .models import Season
from .models import Team, Match, TeamMatch, PlayerMatch, Week, Series, SeriesTeam, TeamMatchBan, MatchCaster, HypeVideo, TeamRole, SeriesPlayer
from .models import PlayerMatchTimeline, PlayerMatchKill, PlayerMatchAssist, PlayerMatchWardPlace, PlayerMatchWardKill, PlayerMatchBuildingKill, PlayerMatchBuildingAssist, PlayerMatchEliteMonsterKill
from .models import Lane, Ward, Building, EliteMonster
from .models import Player
from .models import TeamPlayer
from .models import Role
from .models import Item
from .models import Champion
from .models import SummonerSpell

class PlayerMatchTimelineAdmin(admin.ModelAdmin):
    model = PlayerMatchTimeline

class PlayerMatchKillAdmin(admin.ModelAdmin):
    model = PlayerMatchKill

class PlayerMatchAssistAdmin(admin.ModelAdmin):
    model = PlayerMatchAssist

class PlayerMatchWardPlaceAdmin(admin.ModelAdmin):
    model = PlayerMatchWardPlace

class PlayerMatchWardKillAdmin(admin.ModelAdmin):
    model = PlayerMatchWardKill

class PlayerMatchBuildingKillAdmin(admin.ModelAdmin):
    model = PlayerMatchBuildingKill

class PlayerMatchBuildingAssistAdmin(admin.ModelAdmin):
    model = PlayerMatchBuildingAssist

class PlayerMatchEliteMonsterKillAdmin(admin.ModelAdmin):
    model = PlayerMatchEliteMonsterKill

class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player Info', {'fields': ['name', 'riot_id']}),
    ]
    inlines = [TeamPlayerInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamPlayerInline]

class TeamMatchBanInline(admin.TabularInline):
    model = TeamMatchBan
    extra = 0

class TeamMatchInline(admin.TabularInline):
    model = TeamMatch
    extra = 0

class PlayerMatchInline(admin.TabularInline):
    model = PlayerMatch
    extra = 0

class CasterInline(admin.TabularInline):
    model = MatchCaster
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    inlines = [TeamMatchInline, PlayerMatchInline, TeamMatchBanInline, CasterInline]

class MatchInline(admin.StackedInline):
    model = Match
    extra = 0

class SeriesTeamInline(admin.TabularInline):
    model = SeriesTeam
    extra = 0

class SeriesPlayerInline(admin.TabularInline):
    model = SeriesPlayer
    extra = 0

class SeriesAdmin(admin.ModelAdmin):
    inlines = [MatchInline, SeriesTeamInline, SeriesPlayerInline]

class SeriesInline(admin.StackedInline):
    model = Series
    extra = 0

class WeekAdmin(admin.ModelAdmin):
    inlines = [SeriesInline]

class HypeVideoAdmin(admin.ModelAdmin):
    model = HypeVideo


admin.site.register(Role)
admin.site.register(TeamRole)
admin.site.register(Season)
admin.site.register(Item)
admin.site.register(Champion)
admin.site.register(SummonerSpell)
admin.site.register(PlayerMatchTimeline)
admin.site.register(PlayerMatchKill)
admin.site.register(PlayerMatchAssist)
admin.site.register(PlayerMatchWardPlace)
admin.site.register(PlayerMatchWardKill)
admin.site.register(PlayerMatchBuildingKill)
admin.site.register(PlayerMatchBuildingAssist)
admin.site.register(PlayerMatchEliteMonsterKill)
admin.site.register(Lane)
admin.site.register(Ward)
admin.site.register(Building)
admin.site.register(EliteMonster)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(HypeVideo, HypeVideoAdmin)
