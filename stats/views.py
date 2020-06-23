from django.shortcuts import get_object_or_404, render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Avg, Count, Sum, F, When, Q
from django.utils.timezone import utc
from django.conf import settings
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season, Champion, Match, Week, Series, SeriesTeam, TeamMatch, SeasonChampion, PlayerMatch, Role, TeamRole, SeriesPlayer, Summoner
from .forms import TournamentCodeForm, InitializeMatchForm, CreateRosterForm, LoginForm, EditProfileForm
from get_riot_object import ObjectNotFound, get_item, get_champions, get_champion, get_match, get_all_items, get_match_timeline, update_playermatchkills, update_team_timelines, update_season_timelines, update_team_player_timelines
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import random
import json

def merch(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season
    }
    return render(request, 'stats/merch.html', context)

def team_manager(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season
    }
    return render(request, 'stats/team-manager.html', context)

def email_signup(request):
    latest_season = Season.objects.latest('id')
    context = {
        'season': latest_season
    }
    return render(request, 'stats/email-signup.html', context)

def fun_stats(request):
    latest_season = Season.objects.latest('id')
    top_counterjunglers = latest_season.get_top_counterjunglers()
    most_solo_kills = latest_season.get_most_solo_kills()
    control_ward_pct = latest_season.get_most_percent_control_ward_gold()
    tower_lane_pct = latest_season.lane_first_tower_pct()
    inhib_lane_pct = latest_season.lane_first_inhib_pct()
    dragon_map_pct = latest_season.dragon_map_pct()
    dragon_soul_pct = latest_season.dragon_soul_pct()
    kp_pre_15 = latest_season.get_best_kp_pre_15()
    most_unique_kills = latest_season.get_most_unique_kills()
    most_blue_wards = latest_season.get_most_blue_wards()
    pct_wards_destroyed = latest_season.get_pct_of_opp_wards_destroyed()
    two_drags_pct = latest_season.get_2_drag_win_pct()
    two_rifts_pct = latest_season.get_2_rift_win_pct()
    first_tower_assists = latest_season.get_highest_first_tower_assists()
    cs_diff_below_elo = latest_season.get_cs_diff_below_elo()
    first_bloods = latest_season.get_most_first_bloods()
    damage_per_minute = latest_season.get_damage_per_minute()

    players = Player.objects.all()
    total_kills = sorted(players, key= lambda t: -1 * t.total_kills())
    total_deaths = sorted(players, key= lambda t: -1 * t.total_deaths())
    total_assists = sorted(players, key= lambda t: -1 * t.total_assists())

    context = {
        'season': latest_season,
        'top_counterjunglers': top_counterjunglers,
        'most_solo_kills': most_solo_kills,
        'control_ward_pct': control_ward_pct,
        'tower_lane_pct': tower_lane_pct,
        'inhib_lane_pct': inhib_lane_pct,
        'dragon_map_pct': dragon_map_pct,
        'dragon_soul_pct': dragon_soul_pct,
        'kp_pre_15': kp_pre_15,
        'unique_kills': most_unique_kills,
        'blue_wards': most_blue_wards,
        'pct_wards_destroyed': pct_wards_destroyed,
        'two_drags_pct': two_drags_pct,
        'two_rifts_pct': two_rifts_pct,
        'first_tower_assists': first_tower_assists,
        'cs_diff_below_elo': cs_diff_below_elo,
        'first_bloods': first_bloods,
        'total_kills': total_kills,
        'total_deaths': total_deaths,
        'total_assists': total_assists,
        'damage_per_minute': damage_per_minute
    }
    return render(request, 'stats/fun-stats.html', context)

#def profile(request):
#    latest_season = Season.objects.latest('id')
#    player = get_object_or_404(Player, user=request.user)
#    summoners = Summoner.objects.filter(player=player)
#    if request.method == 'POST':
#        form = EditProfileForm(request.POST, user=request.user)
#        if form.is_valid():
#            new_summoner_name = request.POST['new_summoner']
#            new_summoner = Summoner.objects.create(player=player, name=new_summoner_name)
#            new_summoner.save()
#    else:
#        form = EditProfileForm(user=request.user)
#
#    context = {
#        'season': latest_season,
#        'player': player,
#        'summoners': summoners,
#        'form': form
#    }
#    return render(request, 'stats/profile.html', context)

def create_roster_error(request, series_id):
    latest_season = Season.objects.latest('id')
    series = get_object_or_404(Series, id=series_id)
    context = {
        'season': latest_season,
        'series': series
    }
    return render(request, 'stats/create_roster_error.html', context)


def about(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    return render(request, 'stats/about.html', context)

def head_to_head(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    return render(request, 'stats/head_to_head.html', context)

def faq(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    return render(request, 'stats/faq.html', context)

def season_detail(request, season_id):
    latest_season = Season.objects.latest('id')
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season_id)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())
    next_week = season.next_week()
    context = {
        'latest_season': latest_season,
        'season': season,
        'sorted_teams': sorted_teams,
        'next_week': next_week
    }
    return render(request, 'stats/season.html', context)

def season_players(request, season_id):
    seasons = Season.objects.all().order_by('-id')
    season = get_object_or_404(Season, id=season_id)
    team_players = TeamPlayer.objects.filter(team__season=season_id, role__isFill=False)
    context = {
        'season': season,
        'seasons': seasons,
        'team_players': team_players
    }
    return render(request, 'stats/season_players.html', context)

def latest_season_players(request):
    latest_season = Season.objects.latest('id')
    return season_players(request, latest_season.id)

def season_graphs_empty_detail(request, season_id):
    return season_graphs_detail(request, season_id, "gold", "")

def season_graphs_detail(request, season_id, graph_type, selected_player_id_str):
    if season_id < 3:
        season_id = 3
    selected_players = []
    max_duration = 1
    if selected_player_id_str != "":
        selected_player_ids = selected_player_id_str.split('_')
        selected_players = TeamPlayer.objects.filter(id__in=selected_player_ids)
        for player in selected_players:
            if max_duration == 1 or player.team.get_max_timeline_minute() < max_duration:
                max_duration = player.team.get_max_timeline_minute() 
    max_duration -= 1

    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    season = get_object_or_404(Season, id=season_id)
    roles = Role.objects.filter(isFill=False)
    roles_set = []
    for role in roles:
        roles_set.append({
            'player_set': sorted(TeamPlayer.objects.filter(team__season=season_id, role=role), key= lambda t: t.get_num_matches() * -1),
            'role': role
        })
    top_role = Role.objects.get(name="Top")
    jun_role = Role.objects.get(name="Jungle")
    mid_role = Role.objects.get(name="Mid")
    bot_role = Role.objects.get(name="Bot")
    sup_role = Role.objects.get(name="Support")
    top_players = sorted(TeamPlayer.objects.filter(team__season=season_id, role=top_role), key= lambda t: t.get_num_matches() * -1)
    jun_players = sorted(TeamPlayer.objects.filter(team__season=season_id, role=jun_role), key= lambda t: t.get_num_matches() * -1)
    mid_players = sorted(TeamPlayer.objects.filter(team__season=season_id, role=mid_role), key= lambda t: t.get_num_matches() * -1)
    bot_players = sorted(TeamPlayer.objects.filter(team__season=season_id, role=bot_role), key= lambda t: t.get_num_matches() * -1)
    sup_players = sorted(TeamPlayer.objects.filter(team__season=season_id, role=sup_role), key= lambda t: t.get_num_matches() * -1)
    context = {
        'latest_season': latest_season,
        'season': season,
        'roles': roles_set,
        'selected_players': selected_players,
        'max_duration': max_duration,
        'graph_type': graph_type
    }
    return render(request, 'stats/season_graphs.html', context)


def season_teams_detail(request, season_id):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season_id)
    context = {
        'latest_season': latest_season,
        'season': season,
        'teams': teams
    }
    return render(request, 'stats/season_teams.html', context)

def season_champions_detail(request, season_id):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    season = get_object_or_404(Season, id=season_id)
    champions = SeasonChampion.objects.filter(season=season)
    context = {
        'latest_season': latest_season,
        'season': season,
        'champions': champions
    }
    return render(request, 'stats/season_champions.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    team_players = TeamPlayer.objects.filter(player=player_id)
    context = {
        'player': player,
        'team_players': team_players
    }
    return render(request, 'stats/player.html', context)

def team_recache(request, season_id, team_id):
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(team=team_id)
    for team_player in team_players:
        update_team_player_timelines(team_player.team.id, team_player.player.id, team_player.role.id)
    return redirect('/stats/season/' + season_id + '/team/' + team_id + '/')

def team_detail(request, season_id, team_id):
    team = get_object_or_404(Team, id=team_id, season=season_id)
    seasons = Season.objects.all().order_by('-id')
    team_players = TeamPlayer.objects.filter(team=team_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('role')
    players = Player.objects.filter(teamplayer__team=team).values('id', 'name').distinct()
    all_season_teams = Team.objects.filter(media=team.media).order_by('-id')
    series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    team_roles = TeamRole.objects.filter(team=team).order_by('role')
    kill_timelines = team.get_kill_timelines()
    overall_timelines = team.get_overall_timelines()
    context = {
        'seasons': seasons,
        'team': team,
        'all_season_teams': all_season_teams,
        'team_players': team_players,
        'players': players,
        'roles': team_roles,
	'series_list': series_list,
        'kill_timelines': kill_timelines,
        'overall_timelines': overall_timelines
    }
    return render(request, 'stats/team.html', context)

def team_player_role_detail(request, season_id, team_id, player_id, role_id):
    role = get_object_or_404(Role, id=role_id)
    seasons = Season.objects.all().order_by('-id')
    season = get_object_or_404(Season, id=season_id)
    team = get_object_or_404(Team, id=team_id, season=season_id)
    player = get_object_or_404(Player, id=player_id)
    team_player_role = TeamPlayer.objects.filter(player=player_id, team=team_id, role=role_id)[0]
    team_players = TeamPlayer.objects.filter(player=player_id, team=team_id, role__isFill=False).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion'))
    team_set = TeamPlayer.objects.filter(player=player_id, role__isFill=True).order_by('-team__season')
    teammates = TeamPlayer.objects.filter(team=team, role__isFill=True).exclude(player=player_id)
    #series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    #timelines = team_player_role.get_gold_timeline()
    #enemy_timelines = team_player_role.get_enemy_timelines()
    #max_duration = team.get_max_timeline_minute()
    context = {
        'seasons': seasons,
        'season': season,
        'team': team,
        'player': player,
        'team_player_role': team_player_role,
        'team_players': team_players,
        'team_set': team_set,
        'teammates': teammates
        #'timelines': timelines,
        #'max_duration': max_duration
    }
    return render(request, 'stats/team_player.html', context)

def team_player_detail(request, season_id, team_id, player_id):
    role = get_object_or_404(Role, isFill=True)
    return team_player_role_detail(request, season_id, team_id, player_id, role.id)

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
    return HttpResponseRedirect('/schedule/')

def index(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    teams = Team.objects.filter(season=latest_season)
    context = {
        'seasons': seasons,
        'teams': teams
    }
    return render(request, 'stats/index.html', context)

def schedule(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    seasons = Season.objects.all().order_by('-id')
    teams = Team.objects.filter(season=season_id)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())

    context = {
        'season': season,
        'seasons': seasons,
        'teams': teams,
        'sorted_teams': sorted_teams
    }
    return render(request, 'stats/schedule.html', context)

def latest_schedule(request):
    latest_season = Season.objects.latest('id')
    return schedule(request, latest_season.id)

def standings(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    seasons = Season.objects.all().order_by('-id')
    teams = Team.objects.filter(season=season_id)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())

    context = {
        'season': season,
        'seasons': seasons,
        'teams': teams,
        'sorted_teams': sorted_teams
    }
    return render(request, 'stats/standings.html', context)

def latest_standings(request):
    latest_season = Season.objects.latest('id')
    return standings(request, latest_season.id)

def series_caster_tools(request, season_id, series_id):
    season = get_object_or_404(Season, id=season_id)
    series = get_object_or_404(Series, id=series_id)
    roles = Role.objects.all()
    seriesteams = SeriesTeam.objects.prefetch_related('team__teamplayer_set').filter(series=series)

    context = {
        'season': season,
        'series': series,
        'roles': roles
    }
    return render(request, 'stats/caster_tools.html', context)

def player_matchup(request, blue_player_id, red_player_id, blue_team_id, red_team_id, role_id):
    role = get_object_or_404(Role, id=role_id)

    blue_player = get_object_or_404(TeamPlayer, player=blue_player_id, team=blue_team_id, role=role_id)
    red_player = get_object_or_404(TeamPlayer, player=red_player_id, team=red_team_id, role=role_id)

    max_duration = min(blue_player.team.get_max_timeline_minute(), red_player.team.get_max_timeline_minute()) - 1
    context = {
        'blue_player': blue_player,
        'red_player': red_player,
        'max_duration': max_duration,
        'role': role
    }
    return render(request, 'stats/player_matchup.html', context)


def questions(request, season_id):
    season = get_object_or_404(Season, id=season_id)

    context = {
        'season': season
    }
    return render(request, 'stats/questions.html', context)


def series_head_to_head(request, season_id, series_id):
    series = get_object_or_404(Series, id=series_id)
    seriesteams = SeriesTeam.objects.prefetch_related('team__teamplayer_set').filter(series=series)
    team1 = seriesteams[0]
    team2 = seriesteams[1]

    context = {
        'series': series,
        'team1': team1,
        'team2': team2
    }
    return render(request, 'stats/head_to_head.html', context)


def series_head_to_head_2(request, season_id, series_id):
    series = get_object_or_404(Series, id=series_id)
    seriesteams = SeriesTeam.objects.prefetch_related('team__teamplayer_set').filter(series=series)
    team1 = seriesteams[1]
    team2 = seriesteams[0]

    context = {
        'series': series,
        'team1': team1,
        'team2': team2
    }
    return render(request, 'stats/head_to_head.html', context)

def series_lockin_detail(request, season_id, series_id, team_id):
    if request.method == 'POST':
        form = CreateRosterForm(request.POST, series_id=series_id, team_id=team_id)
        if form.is_valid():
            team = Team.objects.get(id=team_id)
            series = Series.objects.get(id=series_id)
            top = form.cleaned_data.get('top')
            jun = form.cleaned_data.get('jun')
            mid = form.cleaned_data.get('mid')
            bot = form.cleaned_data.get('bot')
            sup = form.cleaned_data.get('sup')
            sub = form.cleaned_data.get('sub')

            SeriesPlayer.objects.filter(series=series, team=team).delete()
            p1 = SeriesPlayer.objects.create(player=top, team=team, series=series, role=Role.objects.get(name='TOP'))
            p2 = SeriesPlayer.objects.create(player=jun, team=team, series=series, role=Role.objects.get(name='JUNGLE'))
            p3 = SeriesPlayer.objects.create(player=mid, team=team, series=series, role=Role.objects.get(name='MID'))
            p4 = SeriesPlayer.objects.create(player=bot, team=team, series=series, role=Role.objects.get(name='BOT'))
            p5 = SeriesPlayer.objects.create(player=sup, team=team, series=series, role=Role.objects.get(name='SUPPORT'))
            if sub is not None:
                p6 = SeriesPlayer.objects.create(player=sub, team=team, series=series, role=Role.objects.get(name='SUBSTITUTE'))
                p6.save()
            p1.save()
            p2.save()
            p3.save()
            p4.save()
            p5.save()
            return HttpResponseRedirect('/season/' + str(season_id) + '/series/' + str(series.id) + '/')

    else:
        form = CreateRosterForm(series_id=series_id, team_id=team_id)

    season = get_object_or_404(Season, id=season_id)
    seasons = Season.objects.all().order_by('-id')
    series = get_object_or_404(Series, id=series_id)
    team = get_object_or_404(Team, id=team_id)
    seriesteam = SeriesTeam.objects.get(series=series, team=team)
    top = Role.objects.get(name = 'TOP')
    jun = Role.objects.get(name = 'JUNGLE')
    mid = Role.objects.get(name = 'MID')
    bot = Role.objects.get(name = 'BOT')
    sup = Role.objects.get(name = 'SUPPORT')
    sub = Role.objects.get(name = 'SUBSTITUTE')
    context = {
            'form': form,
            'season': season,
            'seasons': seasons,
            'series': series,
            'team': team,
            'seriesteam': seriesteam,
            'top': top,
            'jun': jun,
            'mid': mid,
            'bot': bot,
            'sup': sup,
            'sub': sub
    }
    return render(request, 'stats/lock-in.html', context)

def series_detail(request, season_id, series_id):
    season = get_object_or_404(Season, id=season_id)
    seasons = Season.objects.all().order_by('-id')
    series = get_object_or_404(Series, id=series_id)
    roles = Role.objects.filter(isFill=False)
    matches = Match.objects.prefetch_related('playermatch_set').filter(series=series).order_by('game_num')
    seriesteams = SeriesTeam.objects.prefetch_related('team__teamplayer_set').filter(series=series)
    num_match_links = matches.count()
    team1 = seriesteams[0]
    team2 = seriesteams[1]

    user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user

    context = {
        'seasons': seasons,
        'season': season,
        'series': series,
        'roles': roles,
        'matches': matches,
        'num_match_links': num_match_links,
        'team1': team1,
        'team2': team2,
        'now': datetime.utcnow().replace(tzinfo=utc),
        'user': user
    }
    return render(request, 'stats/series.html', context)

def create_roster(request, season_id, series_id, team_id):
    if request.method == 'POST':
        form = CreateRosterForm(request.POST, series_id=series_id, team_id=team_id)
        if form.is_valid():
            s = set()
            top = form.cleaned_data['top']
            jun = form.cleaned_data['jun']
            mid = form.cleaned_data['mid']
            bot = form.cleaned_data['bot']
            sup = form.cleaned_data['sup']
            sub = form.cleaned_data['sub']

            failed = False
            s.add(top)
            if jun in s: 
                failed=True
            s.add(jun)
            if mid in s: 
                failed=True
            s.add(mid)
            if bot in s: 
                failed=True
            s.add(bot)
            if sup in s: 
                failed=True
            s.add(sup)
            if sub in s: 
                failed=True
            s.add(sub)

            if failed:
                return HttpResponseRedirect('/create_roster_error/' + str(series_id) + '/')
            else:
                team = Team.objects.get(id=team_id)
                series = Series.objects.get(id=series_id)
                SeriesPlayer.objects.filter(series=series, team=team).delete()
                p1 = SeriesPlayer.objects.create(player=top, team=team, series=series, role=Role.objects.get(name='Top'))
                p2 = SeriesPlayer.objects.create(player=jun, team=team, series=series, role=Role.objects.get(name='Jungle'))
                p3 = SeriesPlayer.objects.create(player=mid, team=team, series=series, role=Role.objects.get(name='Mid'))
                p4 = SeriesPlayer.objects.create(player=bot, team=team, series=series, role=Role.objects.get(name='Bot'))
                p5 = SeriesPlayer.objects.create(player=sup, team=team, series=series, role=Role.objects.get(name='Support'))
                if sub is not None:
                    p6 = SeriesPlayer.objects.create(player=sub, team=team, series=series, role=Role.objects.get(name='Substitute'))
                    p6.save()
                p1.save()
                p2.save()
                p3.save()
                p4.save()
                p5.save()
                return HttpResponseRedirect('/season/' + str(season_id) + '/series/' + str(series.id) + '/')
    else:
        form = CreateRosterForm(series_id=series_id, team_id=team_id)
    season=Season.objects.get(id=season_id)
    series=Series.objects.get(id=series_id)
    team=Team.objects.get(id=team_id)
    context = {
        'season': season,
        'series': series,
        'team': team,
        'form': form
    }
    return render(request, 'stats/create_roster.html', context)

def create_code(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    jsonRequest = {
        'mapType': match.series.week.season.map_type,
        'metadata': "",
        'pickType': match.series.week.season.pick_type,
        'spectatorType': match.series.week.season.spectator_type,
        'teamSize': match.series.week.season.team_size
    }

    result = {}

    form = InitializeMatchForm(request.POST, series_id=match.series.id)
    code_requester = RiotRequester('/lol/tournament/v4/codes')
    result = code_requester.post('?count=1&tournamentId=' + str(match.series.week.season.tournament_id), jsonRequest)
    match.tournament_code = result[0]
    match.save()

    return HttpResponseRedirect('/stats/season/' + str(match.series.week.season.id) + '/series/' + str(match.series.id) + '/')


#    if request.method == 'POST':
#        blueteam = form.cleaned_data['blue_team']
#        redteam = form.cleaned_data['red_team']
#        for teammatch in TeamMatch.objects.filter(match=match):
#            teammatch.delete()
#        teammatch1 = TeamMatch.objects.create(match=match, team=blueteam, side="blue")
#        teammatch2 = TeamMatch.objects.create(match=match, team=redteam, side="red")
#        for caster in MatchCaster.objects.filter(match=match):
#            caster.delete()
#        for caster in form.cleaned_data['casters']:
#            matchcaster = MatchCaster.objects.create(match=match, player=caster)
#            matchcaster.save()
#        match.save()
#        teammatch1.save()
#        teammatch2.save()
#    else:
#        form = InitializeMatchForm(series_id=match.series.id)
#
#    context = {
#        'match': match,
#        'request': json.dumps(jsonRequest, ensure_ascii=False),
#        'form': form,
#        'result': result
#    }
#    return render(request, 'stats/create_code.html', context)

def load_match(request, season_id, series_id, game_num):
    season = get_object_or_404(Season, id=season_id)
    match = get_object_or_404(Match, series=series_id, game_num=game_num)
    get_match(match.id)
    return redirect('/stats/season/' + season_id + '/series/' + series_id + '/')

def propagate_teams(request):
    teamplayers = TeamPlayer.objects.filter(team__season__id = 6)
    for teamplayer in teamplayers:
        for role in Role.objects.all():
            teamplayerrole = TeamPlayer.objects.filter(team=teamplayer.team, player=teamplayer.player, role=role)
            if not teamplayerrole:
                tpr = TeamPlayer.objects.create(player=teamplayer.player, team=teamplayer.team, role=role)
                tpr.save()
    return render(request, 'stats/index.html')

def match_data_results(request, season_id, series_id, team_1_id, team_2_id, match_id):
    match_result_requester = RiotRequester('/lol/match/v4/matches/')
#    result = match_result_requester.request(str(match_id))
    match = get_match(team_1_id, team_2_id, match_id, series_id)
    context = {
        'result': match
    }
#    try:
#        match = get_match(team_1_id, team_2_id, match_id)
#        match = Match.objects.get(match_id)

    return render(request, 'stats/match_data_results.html', context)

def match_complete(request):
    test_object = TestObject.objects.create()
    test_object.shortCode = request.POST['shortCode']
    test_object.winningTeam = request.POST['winningTeam']
    test_object.losingTeam = request.POST['losingTeam']
    test_object.gameId = request.POST['gameId']
    test_object.save()
    return HttpResponse(status=200)

def loginpage(request):
    seasons = Season.objects.all().order_by('-id')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user = form.login(request)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/stats/schedule/')
    context = {
        'form': form,
        'seasons': seasons
    }
    return render(request, 'stats/login.html', context)
