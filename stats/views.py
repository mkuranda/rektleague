from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import Player, TeamPlayer, Team

def player_detail(request, name):
    player = get_object_or_404(Player, name__iexact=name)
    context = {
        'player': player,
        'team': player.team
    }
    return render(request, 'stats/player.html', context)

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team_players = TeamPlayer.objects.filter(team=team_id)
    context = {
        'team': team,
        'players': team_players,
    }
    return render(request, 'stats/team.html', context)

def index(request):
    team_list = Team.objects.all()
    context = {
        'team_list': team_list,
    }
    return render(request, 'stats/index.html', context)

