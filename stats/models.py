import datetime
from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Player(models.Model):
    summoner_name = models.CharField(max_length=40)
    rank = models.CharField(max_length=15)
    riot_id = models.IntegerField(default=0)
    team = models.ForeignKey(Team)

    def __str__(self):
        return self.summoner_name

