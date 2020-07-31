# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0108_season_playoff_bracket'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerPhotoRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'stats/player_photos')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
        migrations.CreateModel(
            name='SeasonPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elo_value', models.IntegerField(default=100)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
        migrations.CreateModel(
            name='SeasonPlayerRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isMain', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('role', models.ForeignKey(to='stats.Role')),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
        migrations.CreateModel(
            name='TeamInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
