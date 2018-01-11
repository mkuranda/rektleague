# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0018_series_twitch_vod_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermatch',
            name='combat_player_score',
        ),
        migrations.RemoveField(
            model_name='playermatch',
            name='objective_player_score',
        ),
        migrations.RemoveField(
            model_name='playermatch',
            name='total_player_score',
        ),
        migrations.RemoveField(
            model_name='playermatch',
            name='total_score_rank',
        ),
    ]
