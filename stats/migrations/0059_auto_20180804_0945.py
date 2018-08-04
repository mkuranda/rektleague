# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0058_team_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamplayer',
            name='role',
            field=models.ForeignKey(default=None, to='stats.Role'),
        ),
    ]
