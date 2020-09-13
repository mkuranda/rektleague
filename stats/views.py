from django.shortcuts import get_object_or_404, render, redirect
from django import forms
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Avg, Count, Sum, F, When, Q
from django.utils.timezone import utc
from django.conf import settings
from riot_request import RiotRequester
from .models import Player, TeamPlayer, Team, Season, Champion, Match, Week, Series, SeriesTeam, TeamMatch, SeasonChampion, PlayerMatch, Role, TeamRole, SeriesPlayer, Summoner, UserAccount, TeamInvite
from .models import SeasonPlayer, SeasonPlayerRole, PreseasonTeamPlayer, TeamInviteResponse, LeaveTeamNotification
from .forms import TournamentCodeForm, InitializeMatchForm, CreateRosterForm, LoginForm, EditProfileForm, RegisterForm, AddAccountForm, EditAccountForm, RemoveAccountForm, SetMainForm, UpdateUsernameForm, UpdateEmailForm, SeasonSignupForm, ConfirmEloForm
from get_riot_object import ObjectNotFound, get_item, get_champions, get_champion, get_match, get_all_items, get_match_timeline, update_playermatchkills, update_team_timelines, update_season_timelines, update_team_player_timelines
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import random
import json

def get_notifications(user):
    if not user.is_authenticated():
        return []
    userAccount = UserAccount.objects.get(user=user.id, isMain=True)
    invites = TeamInvite.objects.filter(user=user.id)
    count = invites.count()
    teamInviteResponses = []
    leaveTeamNotifications = []
    team = Team.objects.filter(user=user.id)
    if team:
        team = team[0]
        teamInviteResponses = TeamInviteResponse.objects.filter(team=team)
        count += teamInviteResponses.count()
        leaveTeamNotifications = LeaveTeamNotification.objects.filter(team=team)
        count += teamInviteResponses.count()
    notifications = {
        'name': userAccount.name,
        'invites': invites,
        'teamInviteResponses': teamInviteResponses,
        'leaveTeamNotifications': leaveTeamNotifications,
        'count': count
    }
    return notifications

def register(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("/profile")
    else:
        form = RegisterForm()
    context = {
        'seasons': seasons,
        'season': latest_season,
        'form': form,
        'notifications': get_notifications(request.user)
    }        
    return render(request, "stats/register.html", context)

def remove_season_signup(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    seasonPlayer = get_object_or_404(SeasonPlayer, user=request.user, season=season)
    seasonPlayer.delete()
    SeasonPlayerRole.objects.filter(user=request.user, season=season).delete()
    TeamInvite.objects.filter(user=request.user).delete()
    return redirect("/profile/")

def decline_invite(request, team_id, role_id):
    team = get_object_or_404(Team, id=team_id)
    role = get_object_or_404(Role, id=role_id)
    invite = get_object_or_404(TeamInvite, user=request.user, team=team, role=role)
    invite.delete()
    response = TeamInviteResponse.objects.create(user=request.user, team=team, role=role, accepted=False)
    response.save()
    return redirect("/profile/")

def season_signup(request, season_id):
    season = get_object_or_404(Season, id=season_id)
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    accounts = UserAccount.objects.filter(user=request.user.id)
    if request.method == 'POST':
        form = SeasonSignupForm(request.POST)
        if form.is_valid():
            main_role = form.cleaned_data.get('mainRole')
            off_roles = form.cleaned_data.get('offRoles')
            roster_position = form.cleaned_data.get('rosterPosition')
            try:
                seasonPlayer = SeasonPlayer.objects.get(user=request.user)
                seasonPlayer.main_roster = False
                seasonPlayer.substitute = False
            except SeasonPlayer.DoesNotExist:
                seasonPlayer = SeasonPlayer.objects.create(user=request.user, season=season)
            for position in roster_position:
                if position == "1":
                    seasonPlayer.main_roster = True
                if position == "2":
                    seasonPlayer.substitute = True
            seasonPlayer.save()
            SeasonPlayerRole.objects.filter(user=request.user, season=season).delete()
            mainRole = Role.objects.get(id=main_role)
            mainRolePlayer = SeasonPlayerRole.objects.create(user=request.user, season=season, role=mainRole, isMain=True)
            mainRolePlayer.save()
            for off_role in off_roles:
                offRole = Role.objects.get(id=off_role)
                offRolePlayer = SeasonPlayerRole.objects.create(user=request.user, season=season, role=offRole, isMain=False)
                offRolePlayer.save()
            return redirect("/profile/")
    else:
        form = SeasonSignupForm()

    context = {
        'season': season,
        'seasons': seasons,
        'form': form,
        'accounts': accounts,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/season-signup.html', context)

def rules(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/rules.html', context)


def merch(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/merch.html', context)

def team_manager(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    user = request.user.id
    seasonPlayers = SeasonPlayer.objects.filter(season=latest_season)
    teams = Team.objects.filter(season=latest_season, user=user)
    if not teams:
        return redirect('/preseason/' + str(latest_season.id))
    teamReps = []
    for team in teams:
        if team.user != user:
            teamReps.append(team.user)
    unconfirmedPlayers = []
    for seasonPlayer in seasonPlayers:
        if seasonPlayer.elo_value == 100:
            unconfirmedPlayers.append(seasonPlayer.user)
    myPlayers = []
    myInvites = []
    team = None
    if teams:
        team = teams[0]
        myPlayers = PreseasonTeamPlayer.objects.filter(team=team)
        myInvites = TeamInvite.objects.filter(team=team)
    playersOnTeams = TeamPlayer.objects.filter(team__season=latest_season, role__isFill=True, isActive=True)
    roles = Role.objects.all()
    rolePlayers = []
    for role in roles:
        players = []
        if role.isFill:
            players = SeasonPlayer.objects.filter(season=latest_season, substitute=True).exclude(id__in=playersOnTeams).exclude(user__in=teamReps).exclude(user__in=unconfirmedPlayers)
        else:
            playerRoles = SeasonPlayerRole.objects.filter(season=latest_season, role=role).exclude(id__in=playersOnTeams).exclude(user__in=teamReps).exclude(user__in=unconfirmedPlayers)
            myCurrentPlayer = myPlayers.filter(role=role)
            if myCurrentPlayer:
                playerRoles = playerRoles.exclude(Q(user=myCurrentPlayer[0].user) & Q(role=myCurrentPlayer[0].role)).exclude(user__in=teamReps).exclude(user__in=unconfirmedPlayers)
            myCurrentInvite = myInvites.filter(role=role)
            if myCurrentInvite:
                playerRoles = playerRoles.exclude(Q(user=myCurrentInvite[0].user) & Q(role=myCurrentInvite[0].role)).exclude(user__in=teamReps).exclude(user__in=unconfirmedPlayers)
            for playerRole in playerRoles:
                players.append(playerRole.get_season_player())
        myPlayer = PreseasonTeamPlayer.objects.filter(team=team, role=role)
        myInvite = TeamInvite.objects.filter(team=team, role=role)
        if myPlayer:
            myPlayer = myPlayer[0]
        if myInvite:
            myInvite = myInvite[0]
        rolePlayers.append({
                  'name': role.name,
                  'isFill': role.isFill,
                  'icon': role.icon.url,
                  'players': players,
                  'myPlayer': myPlayer,
                  'myInvite': myInvite,
                  'icon_w_name': role.icon_w_name.url,
                  })
    mySubInvites = TeamInvite.objects.filter(team=team, role__isFill=True)
    mySubPlayers = PreseasonTeamPlayer.objects.filter(team=team, role__isFill=True)
    mySubs = [{'invite': None, 'player': None},{'invite': None, 'player': None},{'invite': None, 'player': None}]
    count = 0
    for invite in mySubInvites:
        if count < latest_season.numSubs:
            mySubs[count] = {
                'invite': invite,
                'player': None
                }
            count = count + 1
    for player in mySubPlayers:
        if count < latest_season.numSubs:
            mySubs[count] = {
                'invite': None,
                'player': player
                }
            count = count + 1

    subRole = Role.objects.get(isFill=True)

    context = {
        'seasons': seasons,
        'season': latest_season,
        'roles': rolePlayers,
        'subNums': range(0,latest_season.numSubs),
        'myPlayers': myPlayers,
        'myInvites': myInvites,
        'mySubs': mySubs,
        'team': team,
        'subRole': subRole,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/team-manager.html', context)

def getTeamChanges(role, team, invites, inviteRemoves, removes, player_id):
    player = None
    if player_id != 0:
        player = SeasonPlayer.objects.get(id=player_id)

    current = PreseasonTeamPlayer.objects.filter(team=team, role=role)
    current_invite = TeamInvite.objects.filter(team=team, role=role)
    if current:
        current = current[0]
        if player_id != current.get_season_player().id:
            removes.append({
                'name': current.get_name(),
                'role': role.name,
                'id': current.id
                })
            if player_id != 0:
                invites.append({
                    'name': player.get_name(),
                    'role': role.name,
                    'id': player_id
                    })
    elif current_invite:
        current_invite = current_invite[0]
        if player_id != current_invite.get_season_player().id:
            inviteRemoves.append({
                'name': current_invite.get_name(),
                'role': role.name,
                'id': current_invite.id
                })
            if player_id != 0:
                invites.append({
                    'name': player.get_name(),
                    'role': role.name,
                    'id': player_id
                    })
    elif player_id != 0:
        invites.append({
            'name': player.get_name(),
            'role': role.name,
            'id': player_id
            })

def getSubTeamChanges(team, invites, inviteRemoves, removes, sub1_id, sub2_id, sub3_id):
    current_subs = PreseasonTeamPlayer.objects.filter(team=team, role__isFill=True)
    new_subs = SeasonPlayer.objects.filter(Q(id=sub1_id) | Q(id=sub2_id) | Q(id=sub3_id))
    sub_invites = TeamInvite.objects.filter(team=team, role__isFill=True)

    for sub in new_subs:
        if not current_subs.filter(user=sub.user) and not sub_invites.filter(user=sub.user):
            invites.append({
                'name': sub.get_name(),
                'role': 'SUBSTITUTE',
                'id': sub.id
                })
    for sub in sub_invites:
        if not new_subs.filter(user=sub.user):
            inviteRemoves.append({
                'name': sub.get_name(),
                'role': 'SUBSTITUTE',
                'id': sub.id
                })
    for sub in current_subs:
        if not new_subs.filter(user=sub.user):
            removes.append({
                'name': sub.get_name(),
                'role': 'SUBSTITUTE',
                'id': sub.id
                })

    return

def send_team_invites(request, top_id, jun_id, mid_id, bot_id, sup_id, sub1_id, sub2_id, sub3_id):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    team = Team.objects.filter(user=request.user, season=latest_season)
    if team:
        team = team[0]
    
    invites = []
    inviteRemoves = []
    removes = []

    getTeamChanges(Role.objects.get(name="TOP"), team, invites, inviteRemoves, removes, int(top_id))
    getTeamChanges(Role.objects.get(name="JUNGLE"), team, invites, inviteRemoves, removes, int(jun_id))
    getTeamChanges(Role.objects.get(name="MID"), team, invites, inviteRemoves, removes, int(mid_id))
    getTeamChanges(Role.objects.get(name="BOT"), team, invites, inviteRemoves, removes, int(bot_id))
    getTeamChanges(Role.objects.get(name="SUPPORT"), team, invites, inviteRemoves, removes, int(sup_id))
    getSubTeamChanges(team, invites, inviteRemoves, removes, int(sub1_id), int(sub2_id), int(sub3_id))

    for remove in removes:
        PreseasonTeamPlayer.objects.get(id=remove['id']).delete()

    for inviteRemove in inviteRemoves:
        TeamInvite.objects.get(id=inviteRemove['id']).delete()

    for invite in invites:
        player = SeasonPlayer.objects.get(id=invite['id'])
        role = Role.objects.get(name=invite['role'])
        if player.user == request.user:
            newPlayer = PreseasonTeamPlayer.objects.create(user=player.user, team=team, role=role)
            newPlayer.save()
        else:
            newInvite = TeamInvite.objects.create(user=player.user, team=team, role=role)
            newInvite.save()

    return redirect('/team-manager/')

def team_invite(request, top_id, jun_id, mid_id, bot_id, sup_id, sub1_id, sub2_id, sub3_id):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    team = Team.objects.filter(user=request.user, season=latest_season)
    if team:
        team = team[0]

    invites = []
    inviteRemoves = []
    removes = []

    getTeamChanges(Role.objects.get(name="TOP"), team, invites, inviteRemoves, removes, int(top_id))
    getTeamChanges(Role.objects.get(name="JUNGLE"), team, invites, inviteRemoves, removes, int(jun_id))
    getTeamChanges(Role.objects.get(name="MID"), team, invites, inviteRemoves, removes, int(mid_id))
    getTeamChanges(Role.objects.get(name="BOT"), team, invites, inviteRemoves, removes, int(bot_id))
    getTeamChanges(Role.objects.get(name="SUPPORT"), team, invites, inviteRemoves, removes, int(sup_id))
    getSubTeamChanges(team, invites, inviteRemoves, removes, int(sub1_id), int(sub2_id), int(sub3_id))

    context = {
        'seasons': seasons,
        'season': latest_season,
        'team': team,
        'invites': invites,
        'inviteRemoves': inviteRemoves,
        'removes': removes,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/team-invite-confirm.html', context)

def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    notification = LeaveTeamNotification(team=team, user=request.user)
    notification.save()
    if team.season.isPreseason:
        preseasonTeamPlayer = get_object_or_404(PreseasonTeamPlayer, user=request.user, team=team)
        preseasonTeamPlayer.delete()
        return redirect("/profile/")
    player = get_object_or_404(Player, user=request.user)
    if not team.season.isActive:
        return redirect("/profile/")
    team_players = TeamPlayer.objects.filter(team=team, player=player)
    for team_player in team_players:
        team_player.isActive = False
        team_player.save()
    return redirect("/profile/")

def join_team(request, team_id, role_id):
    team = get_object_or_404(Team, id=team_id)
    role = get_object_or_404(Role, id=role_id)
    invite = get_object_or_404(TeamInvite, user=request.user.id, team=team, role=role)
    if not team.season.isActive:
        return redirect("/profile/")
    preseasonPlayer = PreseasonTeamPlayer.objects.create(user=request.user, team=team, role=role)
    preseasonPlayer.save()
    invites = TeamInvite.objects.filter(user=request.user.id).delete()
    response = TeamInviteResponse.objects.create(user=request.user, team=team, role=role, accepted=True)
    response.save()
    return redirect("/profile/")

def preseason_detail(request, season_id):
    seasons = Season.objects.all().order_by('-id')
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season)
    roles = Role.objects.all()
    teamData = []
    for team in teams:
        teamData.append({
            'team': team,
            'roles': []
            })
        for role in roles:
            if not role.isFill:
               player = PreseasonTeamPlayer.objects.filter(team=team, role=role)
               if player:
                   player = player[0]
                   teamData[-1]['roles'].append({
                       'role': role,
                       'player': player
                       })
               else:
                   teamData[-1]['roles'].append({
                       'role': role,
                       'player': None
                       })
            else:
                subs = PreseasonTeamPlayer.objects.filter(team=team, role__isFill=True)
                for i in range(0, season.numSubs):
                    if subs.count() > i:
                        teamData[-1]['roles'].append({
                            'role': role,
                            'player': subs[i]
                            })
                    else:
                        teamData[-1]['roles'].append({
                            'role': role,
                            'player': None
                            })
    context = {
        'seasons': seasons,
        'season': season,
        'teams': teams,
        'teamData': teamData,
        'roles': roles,
        'subNums': range(0,season.numSubs),
        'notifications': get_notifications(request.user)
    }        
    return render(request, "stats/preseason.html", context)


def profile(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    user = request.user
    accounts = UserAccount.objects.filter(user=request.user.id).order_by('-isMain')
    player = Player.objects.filter(user=user.id)
    if player:
        player = player[0]
    preseasonPlayer = PreseasonTeamPlayer.objects.filter(user=request.user.id, team__season=latest_season)
    if preseasonPlayer:
        preseasonPlayer = preseasonPlayer[0]
    unconfirmedPlayers = []
    if user.is_staff:
        unconfirmedSeasonPlayers = SeasonPlayer.objects.filter(season=latest_season, elo_value=100)
        for unconfirmedSeasonPlayer in unconfirmedSeasonPlayers:
            unconfirmedAccounts = UserAccount.objects.filter(user=unconfirmedSeasonPlayer.user).order_by('-isMain')
            unconfirmedPlayers.append({
                'name': unconfirmedSeasonPlayer.get_name(),
                'id': unconfirmedSeasonPlayer.id,
                'accounts': unconfirmedAccounts,
                })
    seasonPlayer = []
    seasonPlayerRoles = []
    myRepTeam = Team.objects.filter(user=user.id, season=latest_season)
    if myRepTeam:
        myRepTeam = myRepTeam[0]
    seasonPlayer = SeasonPlayer.objects.filter(season=latest_season, user=user.id)
    if seasonPlayer:
        seasonPlayer = seasonPlayer[0]
    seasonPlayerRoles = SeasonPlayerRole.objects.filter(season=latest_season, user=user.id)
    teams = []
    team_players = []
    if player:
        team_players = TeamPlayer.objects.filter(player=player, role__isFill=True, isActive=True)
    for team_player in team_players:
        teams.append(team_player.team)
    editForms = []
    removeForms = []
    setMainForms = []
    confirmEloForms = []
    if request.method == 'POST':
        usernameForm = UpdateUsernameForm(request.POST)
        passwordForm = PasswordChangeForm(request.user, request.POST)
        emailForm = UpdateEmailForm(request.POST)
        addForm = AddAccountForm(request.POST)
        out = passwordForm.is_valid()
        for account in accounts:
            editForms.append(EditAccountForm(request.POST, initial={'account_id': account.id}))
            removeForms.append(RemoveAccountForm(request.POST, initial={'account_id': account.id}))
            setMainForms.append(SetMainForm(request.POST, initial={'account_id': account.id}))
        for unconfirmedPlayer in unconfirmedPlayers:
            confirmEloForms.append(ConfirmEloForm(request.POST, initial={'seasonPlayerId': unconfirmedPlayer['id']}))
        if usernameForm.is_valid() and 'submitUsername' in request.POST:
            if usernameForm.cleaned_data['username']:
                user.username = usernameForm.cleaned_data['username']
                user.save()
            return redirect('/profile')
        if passwordForm.is_valid() and 'submitPassword' in request.POST:
            user = passwordForm.save()
            update_session_auth_hash(request, user)
            return redirect('/signin')
        if emailForm.is_valid() and 'submitEmail' in request.POST:
            if emailForm.cleaned_data['email']:
                user.email = emailForm.cleaned_data['email']
                user.save()
            return redirect('/profile')
        if addForm.is_valid() and 'submitAdd' in request.POST:
            name = addForm.cleaned_data['account_name']
            if name:
                userAccount = UserAccount.objects.create(user=request.user, name=name, isMain=False) 
                userAccount.save()
            return redirect('/profile')
        for editForm, account in zip(editForms, accounts):
            expectedSubmit ='submitEdit' + str(account.id)
            if editForm.is_valid() and expectedSubmit in request.POST:
                if editForm.cleaned_data['account_name']:
                    userAccount = UserAccount.objects.get(id=editForm.cleaned_data['account_id'])
                    userAccount.name = editForm.cleaned_data['account_name']
                    userAccount.save()
                return redirect('/profile')
        for setMainForm, account in zip(setMainForms, accounts):
            expectedSubmit ='submitSetMain' + str(account.id)
            if setMainForm.is_valid() and expectedSubmit in request.POST:
                userAccount = UserAccount.objects.get(id=editForm.cleaned_data['account_id'])
                otherAccounts = UserAccount.objects.filter(user__id=userAccount.user.id)
                for otherAccount in otherAccounts:
                    otherAccount.isMain = False;
                    otherAccount.save()
                userAccount.isMain = True
                userAccount.save()
                return redirect('/profile')
        for removeForm, account in zip(removeForms, accounts):
            expectedSubmit ='submitRemove' + str(account.id)
            if removeForm.is_valid() and expectedSubmit in request.POST:
                userAccount = UserAccount.objects.get(id=removeForm.cleaned_data['account_id'])
                userAccount.delete()
                return redirect('/profile')
        for confirmEloForm, unconfirmedPlayer in zip(confirmEloForms, unconfirmedPlayers):
            confirmEloForm.is_valid()
            expectedSubmit ='submitElo' + str(unconfirmedPlayer['id'])
            elo = confirmEloForm.cleaned_data['elo']
            if confirmEloForm.is_valid() and expectedSubmit in request.POST:
                if confirmEloForm.cleaned_data['elo']:
                    elo = confirmEloForm.cleaned_data['elo']
                    seasonPlayer = SeasonPlayer.objects.get(id=confirmEloForm.cleaned_data['seasonPlayerId'])
                    seasonPlayer.elo_value = elo
                    seasonPlayer.save()
                return redirect('/profile')

    else:
        usernameForm = UpdateUsernameForm()
        passwordForm = PasswordChangeForm(request.user)
        emailForm = UpdateEmailForm()
        addForm = AddAccountForm()
        for account in accounts:
            editForms.append(EditAccountForm(initial={'account_id': account.id}))
            removeForms.append(RemoveAccountForm(initial={'account_id': account.id}))
            setMainForms.append(SetMainForm(initial={'account_id': account.id}))
        for unconfirmedPlayer in unconfirmedPlayers:
            confirmEloForms.append(ConfirmEloForm(initial={'seasonPlayerId': unconfirmedPlayer['id']}))

    confirmEloForms = zip(unconfirmedPlayers, confirmEloForms)
    accountForms = zip(accounts, removeForms, editForms, setMainForms)
    context = {
        'seasons': seasons,
        'season': latest_season,
        'user': user,
        'player': player,
        'preseasonPlayer': preseasonPlayer,
        'teams': teams,
        'accounts': accounts,
        'usernameForm': usernameForm,
        'passwordForm': passwordForm,
        'emailForm': emailForm,
        'addAccountForm': addForm,
        'editForms': editForms,
        'accountForms': accountForms,
        'confirmEloForms': confirmEloForms,
        'seasonPlayer': seasonPlayer,
        'seasonPlayerRoles': seasonPlayerRoles,
        'unconfirmedPlayers': unconfirmedPlayers,
        'myRepTeam': myRepTeam,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/profile.html', context)

def read_response(request, response_id):
    response = get_object_or_404(TeamInviteResponse, id=response_id)
    if response.team.user == request.user:
        response.delete()
    return redirect("/profile/")

def read_leave_team_notification(request, notification_id):
    notification = get_object_or_404(LeaveTeamNotification, id=notification_id)
    if notification.team.user == request.user:
        notification.delete()
    return redirect("/profile/")

def valorant_signup(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/valorant-signup.html', context)

def valorant_thanks(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/valorant-thanks.html', context)

def email_signup(request):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    context = {
        'seasons': seasons,
        'season': latest_season,
        'notifications': get_notifications(request.user)
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
        'damage_per_minute': damage_per_minute,
        'notifications': get_notifications(request.user)
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
        'series': series,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/create_roster_error.html', context)


def about(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/about.html', context)

def head_to_head(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/head_to_head.html', context)

def faq(request):
    latest_season = Season.objects.latest('id')
    context = {
        'latest_season': latest_season,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/faq.html', context)

def season_detail(request, season_id):
    seasons = Season.objects.all().order_by('-id')
    latest_season = Season.objects.latest('id')
    season = get_object_or_404(Season, id=season_id)
    teams = Team.objects.filter(season=season_id)
    sorted_teams = sorted(teams, key= lambda t: t.get_sort_record())
    next_week = season.next_week()
    context = {
        'latest_season': latest_season,
        'season': season,
        'seasons': seasons,
        'sorted_teams': sorted_teams,
        'next_week': next_week,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/season.html', context)

def season_players(request, season_id):
    seasons = Season.objects.all().order_by('-id')
    season = get_object_or_404(Season, id=season_id)
    team_players = TeamPlayer.objects.filter(team__season=season_id, role__isFill=False)
    context = {
        'season': season,
        'seasons': seasons,
        'team_players': team_players,
        'notifications': get_notifications(request.user)
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
        'graph_type': graph_type,
        'notifications': get_notifications(request.user)
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
        'teams': teams,
        'notifications': get_notifications(request.user)
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
        'champions': champions,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/season_champions.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    team_players = TeamPlayer.objects.filter(player=player_id)
    context = {
        'player': player,
        'team_players': team_players,
        'notifications': get_notifications(request.user)
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
    team_players = TeamPlayer.objects.filter(team=team, role__isFill=True)
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
        'roles': team_roles,
	'series_list': series_list,
        'kill_timelines': kill_timelines,
        'overall_timelines': overall_timelines,
        'notifications': get_notifications(request.user)
    }
    return render(request, 'stats/team.html', context)

def team_player_role_detail(request, season_id, team_id, player_id, role_id):
    role = get_object_or_404(Role, id=role_id)
    seasons = Season.objects.all().order_by('-id')
    season = get_object_or_404(Season, id=season_id)
    team = get_object_or_404(Team, id=team_id, season=season_id)
    player = get_object_or_404(Player, id=player_id)
    summoners = player.get_summoners()
    summoner_links = []
    for summoner in summoners:
        summoner_links.append(summoner.name.replace(" ", "+"))
    summoner_data = zip(summoners, summoner_links)
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
        'summoner_data': summoner_data,
        'team_player_role': team_player_role,
        'team_players': team_players,
        'team_set': team_set,
        'teammates': teammates,
        'notifications': get_notifications(request.user),
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
        'champion': champion,
        'notifications': get_notifications(request.user)
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
        'teams': teams,
        'notifications': get_notifications(request.user),
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
        'sorted_teams': sorted_teams,
        'notifications': get_notifications(request.user),
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
        'sorted_teams': sorted_teams,
        'notifications': get_notifications(request.user),
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
        'roles': roles,
        'notifications': get_notifications(request.user),
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
        'role': role,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'stats/player_matchup.html', context)


def questions(request, season_id):
    season = get_object_or_404(Season, id=season_id)

    context = {
        'season': season,
        'notifications': get_notifications(request.user),
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
        'team2': team2,
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
            'sub': sub,
            'notifications': get_notifications(request.user),
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
        'user': user,
        'notifications': get_notifications(request.user),
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
        'form': form,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'stats/create_roster.html', context)

def create_code(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    jsonRequest = {
        'mapType': match.series.week.season.map_type,
        'metadata': "",
        'pickType': match.series.week.season.pick_type,
        'spectatorType': match.series.week.season.spectator_type,
        'teamSize': match.series.week.season.team_size,
        'notifications': get_notifications(request.user),

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
        'result': match,
        'notifications': get_notifications(request.user),
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
                return HttpResponseRedirect('/profile/')
    context = {
        'form': form,
        'seasons': seasons,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'stats/login.html', context)
