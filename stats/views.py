from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Avg, Count, Sum, F, When, Q
from django.utils.timezone import utc
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season, Champion, Match, Week, Series, SeriesTeam, TeamMatch, MatchCaster, SeasonChampion, PlayerMatch, HypeVideo, Role, TeamRole, SeriesPlayer
from .models import HomePageCarouselObject, ArticlePage
from .forms import TournamentCodeForm, InitializeMatchForm, CreateRosterForm
from get_riot_object import ObjectNotFound, get_item, get_champions, get_champion, get_match, get_all_items, get_match_timeline, update_playermatchkills
from datetime import datetime
import random
import json

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

def season_test_detail(request, season_id):
    season = get_object_or_404(Season, id=season_id)

    teams = Team.objects.filter(season=season_id)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())

    standings = []

    i = 1
    for team in sorted_teams:
        standings.append({
            'rank' : i,
            'team' : { 'id' : team.id, 'name' : team.name, 'icon' : team.icon.url },
            'wins' : team.get_wins(),
            'losses' : team.get_losses()
            })
        i = i + 1

    schedule = []

    i = 0
    weeks = season.get_weeks_desc()
    for week in weeks:
        schedule.append({
            'id' : i,
            'name' : week.name_w_title(),
            'series' : [] 
            })
        if week.date:
            schedule[-1].update({'date' : week.date.date().strftime('%B %d, %Y')})
        else:
            schedule[-1].update({'date' : None})

        i = i + 1
        for series in Series.objects.filter(week=week):
            team_1 = series.get_team_1()
            team_2 = series.get_team_2()
            series_team_1 = series.get_series_team_1()
            series_team_2 = series.get_series_team_2()
            schedule[-1]['series'].append({
                'id' : series.id,
                'team_1' : { 
                    'id' : team_1.id,
                    'name' : team_1.name,
                    'wins' : series_team_1.get_wins(),
                    'season_wins' : team_1.get_wins(),
                    'season_losses' : team_1.get_losses(),
                    'icon' : team_1.icon.url
                    },
                'team_2' : { 
                    'id' : team_2.id,
                    'name' : team_2.name,
                    'wins' : series_team_2.get_wins(),
                    'season_wins' : team_2.get_wins(),
                    'season_losses' : team_2.get_losses(),
                    'icon' : team_2.icon.url
                    }
                })

    if season.get_winner():
        winning_team = season.get_winner()[0]
        winner = {
            'id' : winning_team.id,
            'name' : winning_team.name,
            'splash' : winning_team.splash.url
        }
    else:
        winner = None

    context = {
        'season': season.id,
        'banner': season.splash.url,
        'winner': winner,
        'standings': standings,
        'schedule': schedule
    }
    return HttpResponse(json.dumps(context))

def season_players_detail(request, season_id):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season
    }
    season = get_object_or_404(Season, id=season_id)
    team_players = TeamPlayer.objects.filter(team__season=season_id, role__isFill=False)
    context = {
        'latest_season': latest_season,
        'season': season,
        'team_players': team_players
    }
    return render(request, 'stats/season_players.html', context)


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

def team_detail(request, season_id, team_id):
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(team=team_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('role')
    players = Player.objects.filter(teamplayer__team=team).values('id', 'name').distinct()
    series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    team_roles = TeamRole.objects.filter(team=team).order_by('role')
    kill_timelines = team.get_kill_timelines()
    killed_timelines = team.get_killed_timelines()
    overall_timelines = team.get_overall_timelines()
    context = {
        'team': team,
        'team_players': team_players,
        'players': players,
        'roles': team_roles,
	'series_list': series_list,
        'kill_timelines': kill_timelines,
        'killed_timelines': killed_timelines,
        'overall_timelines': overall_timelines
    }
    return render(request, 'stats/team.html', context)

def team_player_detail(request, season_id, team_id, player_id):
    role = get_object_or_404(Role, isFill=True)
    season = get_object_or_404(Season, id=season_id)
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(player=player_id, team=team_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('-role__isFill')
    team_player_role = TeamPlayer.objects.filter(player=player_id, team=team_id, role=role).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion'))[0]
    players = Player.objects.filter(teamplayer__team=team).values('id', 'name').distinct()
    series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    timelines = team_player_role.get_gold_timeline()
    enemy_timelines = team_player_role.get_enemy_timelines()
    max_duration = team.get_max_timeline_minute()
    context = {
        'season': season,
        'team': team,
        'team_players': team_players,
        'team_player_role': team_player_role,
        'players': players,
        'timelines': timelines,
        'max_duration': max_duration
    }
    return render(request, 'stats/team_player.html', context)

def team_player_role_detail(request, season_id, team_id, player_id, role_id):
    season = get_object_or_404(Season, id=season_id)
    team = get_object_or_404(Team, id=team_id, season=season_id)
    team_players = TeamPlayer.objects.filter(player=player_id, team=team_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('-role__isFill')
    team_player_role = TeamPlayer.objects.filter(player=player_id, team=team_id, role=role_id).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion'))[0]
    players = Player.objects.filter(teamplayer__team=team).values('id', 'name').distinct()
    series_list = Series.objects.filter(seriesteam__team = team).order_by('-week__number')
    timelines = team_player_role.get_gold_timeline()
    enemy_timelines = team_player_role.get_enemy_timelines()
    max_duration = team.get_max_timeline_minute()
    context = {
        'season': season,
        'team': team,
        'team_players': team_players,
        'team_player_role': team_player_role,
        'players': players,
        'timelines': timelines,
        'max_duration': max_duration
    }
    return render(request, 'stats/team_player.html', context)

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
    carousel_objects = HomePageCarouselObject.objects.all().exclude(number__isnull=True).order_by('number')
    articles = ArticlePage.objects.all().order_by('-id')[:4]
    featured_players = TeamPlayer.objects.filter(role__isFill=True, team__season=season).exclude(player__photo__isnull=True).exclude(player__photo__exact='').annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('-role__isFill')
    now = datetime.now()
    random.seed(a=(now.day+now.month+now.year+3))
    if len(featured_players) > 0:
        rand = random.randint(0, len(featured_players))
        featured_player = featured_players[rand - 1]
        featured_player_roles = TeamPlayer.objects.filter(player=featured_player.player, team=featured_player.team).annotate(avg_kills=Avg('player__playermatch__kills'), avg_deaths=Avg('player__playermatch__deaths'), avg_assists=Avg('player__playermatch__assists'), num_champs_played=Count('player__playermatch__champion')).order_by('-role__isFill')
    context = {
        'latest_season': season,
        'week': week,
        'teams': teams,
        'carousel_objects': carousel_objects,
        'articles': articles,
        'featured_player': featured_player,
        'featured_player_roles': featured_player_roles
    }
    return render(request, 'stats/news.html', context)

def all_posts(request):
    season = Season.objects.latest('id')
    articles = ArticlePage.objects.all().order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'stats/all_posts.html', context)

def index(request):
    latest_season = Season.objects.latest('id')
    return HttpResponseRedirect('season/' + str(latest_season.id))

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
        'team2': team2,
        'now': datetime.utcnow().replace(tzinfo=utc)
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

def load_match(request, season_id, match_id):
    season = get_object_or_404(Season, id=season_id)
    match = get_object_or_404(Match, id=match_id)
    match = get_match(match_id)
    

#    if request.method == 'POST':
#        form = TournamentCodeForm(request.POST, series_id=series_id)
#        if form.is_valid():
#            match_id_requester = RiotRequester('/lol/match/v3/matches/by-tournament-code/')
#            match_id = match_id_requester.request(form.cleaned_data['tournament_code'] + '/ids')
#            team_1 = Team.objects.filter(name=form.cleaned_data['team_1'])
#            team_2 = Team.objects.filter(name=form.cleaned_data['team_2'])
#            return HttpResponseRedirect('results/' + str(team_1[0].id) + '/' + str(team_2[0].id) + '/' + str(match_id[0]) + '/')
#    else:
#        form = TournamentCodeForm(series_id=series_id)
    context = {
        'season': season,
        'match': match
    }
    return render(request, 'stats/load_match.html', context)

def propagate_teams(request):
    teamplayers = TeamPlayer.objects.filter(team__season__id = 4)
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

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('stats/')
        else:
            return HttpResponseRedirect('stats/disabled_account')
    else:
        return HttpResponseRedirect('stats/invalid_login')

def article(request, url_name):
    content = get_object_or_404(ArticlePage, url_name=url_name)
    file_content = content.content.read()
    context = {
        'content': content,
        'file_content': file_content
    }
    return render(request, 'stats/article.html', context)
    
