# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0024_remove_player_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='map_type',
            field=models.CharField(default='SUMMONERS_RIFT', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='pick_type',
            field=models.CharField(default='TOURNAMENT_DRAFT', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='spectator_type',
            field=models.CharField(default='ALL', max_length=30),
            preserve_default=False,
        ),
    ]
