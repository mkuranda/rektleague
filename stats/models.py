import datetime
from django.db import models
from django.db.models import Count, Avg, Sum, Q, Case, When, F, Value
from django.utils import timezone

class Season(models.Model):
    tournament_id = models.IntegerField(default=0)
    team_size = models.IntegerField(default=5)
    pick_type = models.CharField(max_length=30)
    map_type = models.CharField(max_length=30)
    spectator_type = models.CharField(max_length=30)

    def __str__(self):
        return "Season " + str(self.pk)

    def get_weeks(self):
        return Week.objects.filter(season=self).order_by('-number')

    def get_top_banned(self):
        num_matches = Match.objects.filter(series__week__season=self).exclude(duration=0).count()
        if num_matches == 0:
            return TeamMatchBan.objects.none()
#        return Champion.objects.all().values('name', 'icon', 'teammatchban__champion').annotate(ban_rate=Count('teammatchban__champion') * 100 / num_matches).order_by('-ban_rate')[:6]
        return TeamMatchBan.objects.filter(team__season=self).values('champion__name', 'champion__icon', 'champion').annotate(ban_rate=Count('champion') * 100 / num_matches).order_by('-ban_rate')[:20]

    def get_top_picked(self):
        num_matches = Match.objects.filter(series__week__season=self).exclude(duration=0).count()
        if num_matches == 0:
            return PlayerMatch.objects.none()
#        return Champion.objects.all().values('name', 'icon', 'playermatch__champion').annotate(pick_rate=Count('playermatch__champion') * 100 / num_matches).order_by('-pick_rate')[:6]
        return PlayerMatch.objects.filter(match__series__week__season=self).values('champion__name', 'champion__icon', 'champion').annotate(pick_rate=Count('champion') * 100 / num_matches).order_by('-pick_rate')[:20]

class Week(models.Model):
    season = models.ForeignKey(Season)
    number = models.IntegerField(default=1)

    def __str__(self):
        return str(self.season) + ": Week " + str(self.number)

class Role(models.Model):
    name = models.CharField(max_length=15)
    icon = models.ImageField(upload_to='stats/role/icon', default='')

    def __str__(self):
        return self.name

class Champion(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    icon = models.ImageField(upload_to='stats/champion/icon', default='')

    def __str__(self):
        return self.name

class Series(models.Model):
    twitch_vod_num = models.IntegerField(default=0)
    youtube_link = models.CharField(max_length=100, default='')
    week = models.ForeignKey(Week)
    splash = models.ImageField(upload_to='stats/champion/matchup_splashes', default='')

    def get_team_1(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[0].team

    def get_team_2(self):
	teamSeries = SeriesTeam.objects.filter(series=self)
	return teamSeries[1].team

    def get_team_1_wins(self):
	return TeamMatch.objects.filter(team=self.get_team_1(), win=True, match__series=self).count()

    def get_team_2_wins(self):
	return TeamMatch.objects.filter(team=self.get_team_2(), win=True, match__series=self).count()

    def __str__(self):
	return str(self.week) + ": " + str(self.get_team_1()) + " v " + str(self.get_team_2())


class Match(models.Model):
    series = models.ForeignKey(Series)
    riot_id = models.IntegerField(default=0)
    game_num = models.IntegerField(default=1)
    tournament_code = models.CharField(max_length=100, blank=True)
    duration = models.IntegerField(default=0)

    def get_winner(self):
	return TeamMatch.objects.filter(match=self, win=True)

    def get_loser(self):
	return TeamMatch.objects.filter(match=self, win=False)

    def __str__(self):
        seriesTeams = SeriesTeam.objects.filter(series=self.series)
        return str(seriesTeams[0].team) + " v " + str(seriesTeams[1].team) + " (" + str(self.series.week) + " game " + str(self.game_num) + ")"

class Player(models.Model):
    name = models.CharField(max_length=40)
    riot_id = models.IntegerField(default=0)
    matches = models.ManyToManyField(Match, through='PlayerMatch')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=40)
    players = models.ManyToManyField(Player, through='TeamPlayer')
    matches = models.ManyToManyField(Match, through='TeamMatch')
    season = models.ForeignKey(Season)
    icon = models.ImageField(upload_to='stats')
    splash = models.ImageField(upload_to='stats/team_splashes', default='')

    def get_record(self):
	wins = TeamMatch.objects.filter(team=self, win=True).count()
	losses = TeamMatch.objects.filter(team=self, win=False).exclude(match__duration=0).count()
	return str(wins) + "-" + str(losses)

    def get_sort_record(self):
	wins = TeamMatch.objects.filter(team=self, win=True).count()
	losses = TeamMatch.objects.filter(team=self, win=False).exclude(match__duration=0).count()
	return -1 * ((wins * 100) - losses)

    def get_top_banned(self):
        num_matches = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        return TeamMatchBan.objects.filter(match__teammatch__team=self).exclude(team=self).exclude(match__duration=0).values('champion', 'champion__name', 'champion__icon').annotate(ban_rate=Count('champion') * 100 / num_matches).order_by('-ban_rate')[:6]

    def get_wins(self):
        return TeamMatch.objects.filter(team=self, win=True).exclude(match__duration=0).count()

    def get_losses(self):
        return TeamMatch.objects.filter(team=self, win=False).exclude(match__duration=0).count()

    def get_first_blood_percent(self):
        first_bloods = TeamMatch.objects.filter(team=self, first_blood=True).exclude(match__duration=0).count()
        games = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        return float(first_bloods) * 100 / games

    def get_first_tower_percent(self):
        first_towers = TeamMatch.objects.filter(team=self, first_tower=True).exclude(match__duration=0).count()
        games = TeamMatch.objects.filter(team=self).exclude(match__duration=0).count()
        return float(first_towers) * 100 / games

    def get_tower_kills(self):
        return TeamMatch.objects.filter(team=self).aggregate(Sum('tower_kills'))

    def get_baron_kills(self):
        return TeamMatch.objects.filter(team=self).aggregate(Sum('baron_kills'))

    def __str__(self):
        return self.name

class SeriesTeam(models.Model):
    team = models.ForeignKey(Team)
    series = models.ForeignKey(Series)

    class Meta:
        unique_together = (("team", "series"))
    
    def get_wins(self):
	return TeamMatch.objects.filter(team=self.team, win=True, match__series=series).exclude(match__duration=0).count()


class PlayerRole(models.Model):
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    priority = models.IntegerField(default=10)

    class Meta:
        unique_together = (("player", "role"))

class PlayerMatch(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    champion = models.ForeignKey(Champion)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    physical_damage_dealt = models.IntegerField(default=0)
    neutral_minions_killed_team_jungle = models.IntegerField(default=0)
    magic_damage_dealt = models.IntegerField(default=0)
    neutral_minions_killed_enemy_jungle = models.IntegerField(default=0)
    largest_critical_strike = models.IntegerField(default=0)
    total_damage_dealt = models.IntegerField(default=0)
    magic_damage_dealt_to_champions = models.IntegerField(default=0)
    vision_wards_bought_in_game = models.IntegerField(default=0)
    damage_dealt_to_objectives = models.IntegerField(default=0)
    largest_killing_spree = models.IntegerField(default=0)
    double_kills = models.IntegerField(default=0)
    triple_kills = models.IntegerField(default=0)
    quadra_kills = models.IntegerField(default=0)
    penta_kills = models.IntegerField(default=0)
    total_time_crowd_control_dealt = models.IntegerField(default=0)
    longest_time_spent_living = models.IntegerField(default=0)
    wards_killed = models.IntegerField(default=0)
    first_tower_assist = models.BooleanField(default=False)
    first_tower_kill = models.BooleanField(default=False)
    first_blood_assist = models.BooleanField(default=False)
    vision_score = models.IntegerField(default=0)
    wards_placed = models.IntegerField(default=0)
    turret_kills = models.IntegerField(default=0)
    damage_self_mitigated = models.IntegerField(default=0)
    champ_level = models.IntegerField(default=0)
    first_inhibitor_kill = models.BooleanField(default=False)
    gold_earned = models.IntegerField(default=0)
    magical_damage_taken = models.IntegerField(default=0)
    true_damage_taken = models.IntegerField(default=0)
    first_inhibitor_assist = models.BooleanField(default=False)
    neutral_minions_killed = models.IntegerField(default=0)
    damage_dealt_to_turrets = models.IntegerField(default=0)
    physical_damage_dealt_to_champions = models.IntegerField(default=0)
    gold_spent = models.IntegerField(default=0)
    true_damage_dealt = models.IntegerField(default=0)
    true_damage_dealt_to_champions = models.IntegerField(default=0)
    total_heal = models.IntegerField(default=0)
    total_minions_killed = models.IntegerField(default=0)
    first_blood_kill = models.BooleanField(default=False)
    sight_wards_bought_in_game = models.IntegerField(default=0)
    total_damage_dealt_to_champions = models.IntegerField(default=0)
    inhibitor_kills = models.IntegerField(default=0)
    total_damage_taken = models.IntegerField(default=0)
    killing_sprees = models.IntegerField(default=0)
    time_ccing_others = models.IntegerField(default=0)
    physical_damage_taken = models.IntegerField(default=0)

    class Meta:
        unique_together = (("player", "match"))

    def win(self):
        return match.get_winner == player.team

    def get_cs(self):
        return self.neutral_minions_killed + self.total_minions_killed

class TeamPlayer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    isLeader = models.BooleanField(default=False)

    class Meta:
        unique_together = (("team", "player"))
    
    def get_player(self):
        return Player.objects.filter(pk=self.player)

    def get_team(self):
        return Team.objects.filter(pk=self.team)

    def get_avg_kills(self):
        avg_kills = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_kills=Avg('playermatch__kills'))['avg_kills']
        if avg_kills == None:
            return 0
        return avg_kills

    def get_avg_deaths(self):
        avg_deaths = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_deaths=Avg('playermatch__deaths'))['avg_deaths']
        if avg_deaths == None:
            return 0
        return avg_deaths

    def get_avg_assists(self):
        avg_assists = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(avg_assists=Avg('playermatch__assists'))['avg_assists']
        if avg_assists == None:
            return 0
        return avg_assists

    def get_kda(self):
        kda = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(kda=Avg((F('playermatch__kills') + F('playermatch__assists')) / F('playermatch__deaths')))['kda']
#        kda = PlayerMatch.objects.filter(player=self.player).aggregate(kda=Avg((F('kills') + F('assists')) / F('deaths')))
        if kda == None:
            return 0
        return kda

    def get_cs_per_game(self):
        cs = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(cs=Avg((F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed'))))['cs']
#        kda = PlayerMatch.objects.filter(player=self.player).aggregate(kda=Avg((F('kills') + F('assists')) / F('deaths')))
        if cs == None:
            return 0
        return cs 

    def get_kill_participation(self):
#        total_kills = PlayerMatch.objects.filter(player__team=self.team).aggregate(Sum('kills'))['kills__sum']
        total_kills = TeamMatch.objects.filter(team=self.team).aggregate(kills__sum=Sum('match__playermatch__kills'))['kills__sum']
#        player_kills_assists = PlayerMatch.objects.filter(player=self.player).aggregate(kills__sum=Sum(F('kills') + F('assists')))['kills__sum']
        player_kills_assists = Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).aggregate(kills__sum=Sum(F('playermatch__kills') + F('playermatch__assists')))['kills__sum']
        if player_kills_assists == None:
            return 0
        return 100.0 * player_kills_assists / total_kills

    def get_played_champion_list(self):
        return Match.objects.select_related().filter(playermatch__player=self.player, teammatch__team=self.team).values('playermatch__champion', 'playermatch__champion__name', 'playermatch__champion__icon').annotate(champion_count=Count('playermatch__champion'), average_vision_score=Avg('playermatch__vision_score'), avg_kills=Avg('playermatch__kills'), avg_deaths=Avg('playermatch__deaths'), avg_assists=Avg('playermatch__assists'), winrate=Avg(F('teammatch__win') * 100), average_cs=Avg(F('playermatch__neutral_minions_killed') + F('playermatch__total_minions_killed'))).order_by('-champion_count')


class TeamMatch(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    side = models.CharField(max_length=5)
    win = models.BooleanField(default=False)
    first_dragon = models.BooleanField(default=False)
    first_inhibitor = models.BooleanField(default=False)
    baron_kills = models.IntegerField(default=0)
    first_rift_herald = models.BooleanField(default=False)
    first_blood = models.BooleanField(default=False)
    first_tower = models.BooleanField(default=False)
    inhibitor_kills = models.IntegerField(default=0)
    tower_kills = models.IntegerField(default=0)

    class Meta:
        unique_together = (("team", "match"))

    def get_player_matches(self):
        return PlayerMatch.objects.filter(match=self.match, player__team=self.team)

    def get_team_bans(self):
        return TeamMatchBan.objects.filter(match=self.match, team=self.team)

class TeamMatchBan(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    champion = models.ForeignKey(Champion)
    pickTurn = models.IntegerField(default=0)

    class Meta:
        ordering = ["champion"]

class Item(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    icon = models.ImageField(upload_to='stats/item/icon', default='')

class PlayerMatchItem(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    item = models.ForeignKey(Item)

class SummonerSpell(models.Model):
    riot_id = models.IntegerField(default=0)
    name = models.CharField(max_length=20)
    icon = models.ImageField(upload_to='stats/summoner-spell/icon', default='')

class PlayerMatchSummonerSpell(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    summoner_spell = models.ForeignKey(SummonerSpell)


class MatchCaster(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
