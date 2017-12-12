from django.contrib import admin

from .models import Season
from .models import Team
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


admin.site.register(Role)
admin.site.register(Season)
admin.site.register(Item)
admin.site.register(Champion)
admin.site.register(SummonerSpell)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
