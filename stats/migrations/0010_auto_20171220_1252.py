# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_auto_20171220_1247'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TeamSeries',
            new_name='SeriesTeam',
        ),
    ]
