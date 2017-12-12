# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_player_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('riot_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('riot_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('riot_id', models.IntegerField(default=0)),
                ('tournament_code', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kills', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('champion', models.ForeignKey(to='stats.Champion')),
                ('match', models.ForeignKey(to='stats.Match')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(to='stats.Item')),
                ('match', models.ForeignKey(to='stats.Match')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchSummonerSpell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match', models.ForeignKey(to='stats.Match')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('riot_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('side', models.CharField(max_length=5)),
                ('win', models.BooleanField()),
                ('match', models.ForeignKey(to='stats.Match')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMatchBan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pickTurn', models.IntegerField(default=0)),
                ('champion', models.ForeignKey(to='stats.Champion')),
                ('match', models.ForeignKey(to='stats.Match')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isLeader', models.BooleanField()),
            ],
        ),
        migrations.RenameField(
            model_name='player',
            old_name='summoner_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='player',
            name='role',
        ),
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='role',
            field=models.ForeignKey(to='stats.Role'),
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='team',
            field=models.ForeignKey(to='stats.Team'),
        ),
        migrations.AddField(
            model_name='playerrole',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AddField(
            model_name='playerrole',
            name='role',
            field=models.ForeignKey(to='stats.Role'),
        ),
        migrations.AddField(
            model_name='playermatchsummonerspell',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AddField(
            model_name='playermatchsummonerspell',
            name='summoner_spell',
            field=models.ForeignKey(to='stats.SummonerSpell'),
        ),
        migrations.AddField(
            model_name='playermatchitem',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AddField(
            model_name='playermatch',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together=set([('team', 'player')]),
        ),
        migrations.AlterUniqueTogether(
            name='teammatch',
            unique_together=set([('team', 'match')]),
        ),
        migrations.AlterUniqueTogether(
            name='playerrole',
            unique_together=set([('player', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='playermatch',
            unique_together=set([('player', 'match')]),
        ),
    ]
