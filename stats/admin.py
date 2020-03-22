from django.contrib import admin

from .models import Season, Summoner
from .models import Team, Match, TeamMatch, PlayerMatch, Week, Series, SeriesTeam, TeamMatchBan, TeamRole, SeriesPlayer, TeamMedia
from .models import PlayerMatchTimeline, PlayerMatchKill, PlayerMatchAssist, PlayerMatchWardPlace, PlayerMatchWardKill, PlayerMatchBuildingKill, PlayerMatchBuildingAssist, PlayerMatchEliteMonsterKill
from .models import Lane, Ward, Building, EliteMonster
from .models import Player
from .models import TeamPlayer
from .models import Role
from .models import Item
from .models import Champion
from .models import TeamTimeline, SeasonTimeline, TeamPlayerTimeline

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

class SummonerAdmin(admin.ModelAdmin):
    model = Summoner 

class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 1

class SummonerInline(admin.TabularInline):
    model = Summoner
    extra = 1

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Player Info', {'fields': ['name', 'riot_id', 'photo', 'elo_value']}),
    ]
    inlines = [TeamPlayerInline, SummonerInline]

class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamPlayerInline]

class TeamMatchBanInline(admin.TabularInline):
    model = TeamMatchBan
    extra = 0

class TeamMatchInline(admin.TabularInline):
    model = TeamMatch
    extra = 2

class PlayerMatchInline(admin.TabularInline):
    model = PlayerMatch
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    inlines = [TeamMatchInline, PlayerMatchInline, TeamMatchBanInline]

class MatchInline(admin.StackedInline):
    model = Match
    extra = 0

class SeriesTeamInline(admin.TabularInline):
    model = SeriesTeam
    extra = 2

class SeriesPlayerInline(admin.TabularInline):
    model = SeriesPlayer
    extra = 6

class SeriesAdmin(admin.ModelAdmin):
    inlines = [MatchInline, SeriesTeamInline, SeriesPlayerInline]

class SeriesInline(admin.StackedInline):
    model = Series
    extra = 0

class WeekAdmin(admin.ModelAdmin):
    inlines = [SeriesInline]

admin.site.register(Role)
admin.site.register(TeamRole)
admin.site.register(Season)
admin.site.register(Item)
admin.site.register(Champion)
admin.site.register(PlayerMatchTimeline)
admin.site.register(PlayerMatchKill)
admin.site.register(PlayerMatchAssist)
admin.site.register(PlayerMatchWardPlace)
admin.site.register(PlayerMatchWardKill)
admin.site.register(PlayerMatchBuildingKill)
admin.site.register(PlayerMatchBuildingAssist)
admin.site.register(PlayerMatchEliteMonsterKill)
admin.site.register(Summoner)
admin.site.register(Lane)
admin.site.register(Ward)
admin.site.register(Building)
admin.site.register(EliteMonster)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(TeamTimeline)
admin.site.register(SeasonTimeline)
admin.site.register(TeamPlayerTimeline)
admin.site.register(TeamMedia)
