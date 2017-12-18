from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season, Champion, Match, Week
from .forms import TournamentCodeForm
from get_riot_object import ObjectNotFound, get_item, get_champion, get_match

def about(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    return render(request, 'stats/about.html', context)

def faq(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    return render(request, 'stats/faq.html', context)

def season_detail(request, season_id):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season_id)
    context = {
        'latest_season': latest_season,
        'season': season,
        'teams': teams,
    }
    return render(request, 'stats/season.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    team_players = TeamPlayer.objects.filter(player=player_id)
    context = {
        'player': player,
        'team_players': team_players
    }
    return render(request, 'stats/player.html', context)

def team_detail(request, season_id, team_id):
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(team=team_id)
    context = {
        'team': team,
        'players': team_players,
    }
    return render(request, 'stats/team.html', context)

def champion_detail(request, champion_id):
    try:
        champion = get_champion(champion_id)
    except ObjectNotFound:
        raise Http404("Champion does not exist")
    context = {
        'champion': champion
    }
    return render(request, 'stats/champion.html', context)


def news(request):
    latest_season = Season.objects.latest('id')
    week = Week.objects.filter(season=latest_season).latest('id')
    teams = Team.objects.filter(season=latest_season)
    matches = Match.objects.filter(week=week)
    context = {
        'week': week,
        'teams': teams,
        'matches': matches,
        'latest_season': latest_season
    }
    return render(request, 'stats/news.html', context)


def index(request):
    return HttpResponseRedirect('news/')

def load_match(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    if request.method == 'POST':
        form = TournamentCodeForm(request.POST)
        if form.is_valid():
            match_id_requester = RiotRequester('/lol/match/v3/matches/by-tournament-code/')
            match_id = match_id_requester.request(form.cleaned_data['tournament_code'] + '/ids')
            team_1 = Team.objects.filter(name=form.cleaned_data['team_1'])
            team_2 = Team.objects.filter(name=form.cleaned_data['team_2'])
            return HttpResponseRedirect('results/' + str(team_1[0].id) + '/' + str(team_2[0].id) + '/' + str(match_id[0]) + '/')
    else:
        form = TournamentCodeForm()
    context = {
        'season': season,
        'form': form,
    }
    return render(request, 'stats/load_match.html', context)


def match_data_results(request, season_id, team_1_id, team_2_id, match_id):
    match_result_requester = RiotRequester('/lol/match/v3/matches/')
#    result = match_result_requester.request(str(match_id))
    match = get_match(team_1_id, team_2_id, match_id)
    context = {
        'result': match
    }
#    try:
#        match = get_match(team_1_id, team_2_id, match_id)
#        match = Match.objects.get(match_id)

    return render(request, 'stats/match_data_results.html', context)


