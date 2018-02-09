from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Avg, Count, Sum, F, When, Q
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season, Champion, Match, Week, Series, SeriesTeam, TeamMatch, MatchCaster
from .forms import TournamentCodeForm, InitializeMatchForm
from get_riot_object import ObjectNotFound, get_item, get_champion, get_match, get_all_items
import json

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
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())
    context = {
        'latest_season': latest_season,
        'season': season,
        'sorted_teams': sorted_teams
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
    team_players = TeamPlayer.objects.filter(team=team_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion'))
    series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    context = {
        'team': team,
        'players': team_players,
	'series_list': series_list
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

def get_items(request):
    try:
        get_all_items(1)
    except ObjectNotFound:
        raise Http404("Items do not exist")
    return HttpResponseRedirect('news/')

def news(request):
    season = Season.objects.latest('id')
    week = Week.objects.filter(season=season).latest('id')
    teams = Team.objects.filter(season=season)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())
    series_list = Series.objects.filter(week=week)

    context = {
        'latest_season': season,
        'week': week,
        'teams': sorted_teams,
	'series_list': series_list
    }
    return render(request, 'stats/news.html', context)

def index(request):
    return HttpResponseRedirect('news/')

def series_detail(request, season_id, series_id):
    season = get_object_or_404(Season, id=season_id)
    series = get_object_or_404(Series, id=series_id)
    matches = Match.objects.prefetch_related('playermatch_set').filter(series=series).order_by('game_num')
    seriesteams = SeriesTeam.objects.prefetch_related('team__teamplayer_set').filter(series=series)
    num_match_links = matches.count()
    team1 = seriesteams[0]
    team2 = seriesteams[1]

    context = {
        'season': season,
        'series': series,
        'matches': matches,
        'num_match_links': num_match_links,
        'team1': team1,
        'team2': team2 
    }
    return render(request, 'stats/series.html', context)

def create_code(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    jsonRequest = {
        'allowedSummonerIds': [
            ],
        'mapType': match.series.week.season.map_type,
        'metadata': "",
        'pickType': match.series.week.season.pick_type,
        'spectatorType': match.series.week.season.spectator_type,
        'teamSize': match.series.week.season.team_size
    }

    players = TeamPlayer.objects.select_related().filter(Q(team=match.series.get_team_1()) | Q(team=match.series.get_team_2()))

    result = {}

    for player in players:
        jsonRequest['allowedSummonerIds'].append(player.player.riot_id)

    if request.method == 'POST':
        form = InitializeMatchForm(request.POST, series_id=match.series.id)
        if form.is_valid():
            for caster in form.cleaned_data['casters']:
                jsonRequest['allowedSummonerIds'].append(caster.riot_id)
        code_requester = RiotRequester('/lol/tournament/v3/codes')
        result = code_requester.post('?count=1&tournamentId=' + str(match.series.week.season.tournament_id), jsonRequest)
        match.tournament_code = result[0]
        blueteam = form.cleaned_data['blue_team']
        redteam = form.cleaned_data['red_team']
        for teammatch in TeamMatch.objects.filter(match=match):
            teammatch.delete()
        teammatch1 = TeamMatch.objects.create(match=match, team=blueteam, side="blue")
        teammatch2 = TeamMatch.objects.create(match=match, team=redteam, side="red")
        for caster in MatchCaster.objects.filter(match=match):
            caster.delete()
        for caster in form.cleaned_data['casters']:
            matchcaster = MatchCaster.objects.create(match=match, player=caster)
            matchcaster.save()
        match.save()
        teammatch1.save()
        teammatch2.save()
    else:
        form = InitializeMatchForm(series_id=match.series.id)

    context = {
        'match': match,
        'request': json.dumps(jsonRequest, ensure_ascii=False),
        'form': form,
        'result': result
    }
    return render(request, 'stats/create_code.html', context)

def load_match(request, season_id, series_id):
    season = get_object_or_404(Season, id=season_id)
    series = get_object_or_404(Series, id=series_id)
    if request.method == 'POST':
        form = TournamentCodeForm(request.POST, series_id=series_id)
        if form.is_valid():
            match_id_requester = RiotRequester('/lol/match/v3/matches/by-tournament-code/')
            match_id = match_id_requester.request(form.cleaned_data['tournament_code'] + '/ids')
            team_1 = Team.objects.filter(name=form.cleaned_data['team_1'])
            team_2 = Team.objects.filter(name=form.cleaned_data['team_2'])
            return HttpResponseRedirect('results/' + str(team_1[0].id) + '/' + str(team_2[0].id) + '/' + str(match_id[0]) + '/')
    else:
        form = TournamentCodeForm(series_id=series_id)
    context = {
        'season': season,
	'series': series,
        'form': form,
    }
    return render(request, 'stats/load_match.html', context)


def match_data_results(request, season_id, series_id, team_1_id, team_2_id, match_id):
    match_result_requester = RiotRequester('/lol/match/v3/matches/')
#    result = match_result_requester.request(str(match_id))
    match = get_match(team_1_id, team_2_id, match_id, series_id)
    context = {
        'result': match
    }
#    try:
#        match = get_match(team_1_id, team_2_id, match_id)
#        match = Match.objects.get(match_id)

    return render(request, 'stats/match_data_results.html', context)


