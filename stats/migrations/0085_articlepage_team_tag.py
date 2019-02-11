# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0084_auto_20190121_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='team_tag',
            field=models.ManyToManyField(to='stats.Team'),
        ),
    ]
