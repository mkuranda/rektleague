import datetime
from django.db import models
from django.utils import timezone

class Season(models.Model):
    tournament_id = models.IntegerField(default = 0)
    team_size = models.IntegerField(default = 5)

    def __str__(self):
        return "Season " + str(self.pk)

class Role(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Champion(models.Model):
    riot_id = models.IntegerField(default=0)
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=40)

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
    isLeader = models.BooleanField()

    class Meta:
        unique_together = (("team", "role"), ("team", "player"))
    
    def get_player(self):
        return Player.objects.filter(pk=self.player)

    def get_team(self):
        return Team.objects.filter(pk=self.team)

class Match(models.Model):
    riot_id = models.IntegerField(default=0)
    tournament_code = models.CharField(max_length=40)


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

    class Meta:
        unique_together = (("player", "match"))

class TeamMatch(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    side = models.CharField(max_length=5)
    win = models.BooleanField()

    class Meta:
        unique_together = (("team", "match"))

class TeamMatchBan(models.Model):
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match)
    champion = models.ForeignKey(Champion)
    pickTurn = models.IntegerField(default=0)

class Item(models.Model):
    riot_id = models.IntegerField(default=0)
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









