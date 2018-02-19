# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0028_team_splash'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='riot_id',
            field=models.IntegerField(default=0),
        ),
    ]
