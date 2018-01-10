# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0015_auto_20171230_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='matches',
            field=models.ManyToManyField(to='stats.Match', through='stats.PlayerMatch'),
        ),
        migrations.AddField(
            model_name='team',
            name='matches',
            field=models.ManyToManyField(to='stats.Match', through='stats.TeamMatch'),
        ),
        migrations.AddField(
            model_name='team',
            name='players',
            field=models.ManyToManyField(to='stats.Player', through='stats.TeamPlayer'),
        ),
    ]
