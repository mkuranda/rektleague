# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0101_auto_20200203_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='team_tag',
        ),
        migrations.DeleteModel(
            name='HomePageCarouselObject',
        ),
        migrations.RemoveField(
            model_name='matchcaster',
            name='match',
        ),
        migrations.RemoveField(
            model_name='matchcaster',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchsummonerspell',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchsummonerspell',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchsummonerspell',
            name='summoner_spell',
        ),
        migrations.DeleteModel(
            name='TestObject',
        ),
        migrations.AddField(
            model_name='player',
            name='elo_value',
            field=models.IntegerField(default=100),
        ),
        migrations.DeleteModel(
            name='ArticlePage',
        ),
        migrations.DeleteModel(
            name='MatchCaster',
        ),
        migrations.DeleteModel(
            name='PlayerMatchSummonerSpell',
        ),
        migrations.DeleteModel(
            name='SummonerSpell',
        ),
    ]
