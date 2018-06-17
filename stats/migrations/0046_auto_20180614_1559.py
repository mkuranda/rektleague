# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0045_playermatch_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerMatchAssist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchBuildingAssist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchBuildingKill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('building_type', models.IntegerField(choices=[(0, b'outer_tower'), (1, b'inner_tower'), (2, b'base_tower'), (3, b'nexus_tower'), (4, b'inhibitor')])),
                ('lane', models.IntegerField(choices=[(0, b'TOP'), (1, b'MID'), (2, b'BOT')])),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchEliteMonsterKill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('monster_type', models.IntegerField(choices=[(0, b'rift_herald'), (1, b'infernal_dragon'), (2, b'mountain_dragon'), (3, b'cloud_dragon'), (4, b'ocean_dragon'), (5, b'elder_dragon'), (5, b'baron')])),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchKill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('killer', models.ForeignKey(to='stats.Player')),
                ('match', models.ForeignKey(to='stats.Match')),
                ('victim', models.ForeignKey(related_name='victim', to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchTimeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('level', models.IntegerField(default=1)),
                ('gold', models.IntegerField(default=0)),
                ('minions_killed', models.IntegerField(default=0)),
                ('monsters_killed', models.IntegerField(default=0)),
                ('position_x', models.IntegerField()),
                ('position_y', models.IntegerField()),
                ('xp', models.IntegerField(default=0)),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchWardKill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('ward_type', models.IntegerField(choices=[(0, b'undefined'), (1, b'yellow_trinket'), (2, b'control_ward'), (3, b'sight_ward')])),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatchWardPlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('ward_type', models.IntegerField(choices=[(0, b'undefined'), (1, b'yellow_trinket'), (2, b'control_ward'), (3, b'sight_ward')])),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.AddField(
            model_name='playermatchbuildingassist',
            name='kill',
            field=models.ForeignKey(to='stats.PlayerMatchBuildingKill'),
        ),
        migrations.AddField(
            model_name='playermatchbuildingassist',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
        migrations.AddField(
            model_name='playermatchassist',
            name='kill',
            field=models.ForeignKey(to='stats.PlayerMatchKill'),
        ),
        migrations.AddField(
            model_name='playermatchassist',
            name='player',
            field=models.ForeignKey(to='stats.Player'),
        ),
    ]
