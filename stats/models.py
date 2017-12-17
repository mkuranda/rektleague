import datetime
from django.db import models
from django.utils import timezone

class Season(models.Model):
    tournament_id = models.IntegerField(default = 0)
    team_size = models.IntegerField(default = 5)

    def __str__(self):
        return "Season " + str(self.pk)

class Week(models.Model):
    season = models.ForeignKey(Season)

    def __str__(self):
	seasonWeeks = Week.objects.filter(season=self.season).order_by('id')
	return "Week " + str(self.id - seasonWeeks[0].id + 1)

class Role(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Champion(models.Model):
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=40)
    season = models.ForeignKey(Season)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=40)
    rank = models.CharField(max_length=15)
    riot_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TeamPlayer(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    role = models.ForeignKey(Role)
    isLeader = models.BooleanField(default=False)

    class Meta:
        unique_together = (("team", "role"), ("team", "player"))
    
    def get_player(self):
        return Player.objects.filter(pk=self.player)

    def get_team(self):
        return Team.objects.filter(pk=self.team)

class Match(models.Model):
    week = models.ForeignKey(Week)
    tournament_code = models.CharField(max_length=40)
    duration = models.IntegerField(default=0)

    def __str__(self):
        teamMatches = TeamMatch.objects.filter(match=self)
        return str(teamMatches[0].team) + " v " + str(teamMatches[1].team)

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
    total_player_score = models.IntegerField(default=0)
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
    objective_player_score = models.IntegerField(default=0)
    combat_player_score = models.IntegerField(default=0)
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
    total_score_rank = models.IntegerField(default=0)
    total_damage_taken = models.IntegerField(default=0)
    killing_sprees = models.IntegerField(default=0)
    time_ccing_others = models.IntegerField(default=0)
    physical_damage_taken = models.IntegerField(default=0)

    class Meta:
        unique_together = (("player", "match"))

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

class TeamMatchBan(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    champion = models.ForeignKey(Champion)
    pickTurn = models.IntegerField(default=0)

class Item(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=40)

class PlayerMatchItem(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    item = models.ForeignKey(Item)

class SummonerSpell(models.Model):
    riot_id = models.IntegerField(default=0)
    name = models.CharField(max_length=20)

class PlayerMatchSummonerSpell(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    summoner_spell = models.ForeignKey(SummonerSpell)



