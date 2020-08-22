# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0118_season_ispreseason'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonplayer',
            name='main_roster',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seasonplayer',
            name='substitute',
            field=models.BooleanField(default=False),
        ),
    ]
