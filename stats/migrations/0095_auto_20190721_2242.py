# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0094_seasontimeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamplayer',
            name='csDiffAt15',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='csPerMin',
            field=models.FloatField(default=0),
        ),
    ]
