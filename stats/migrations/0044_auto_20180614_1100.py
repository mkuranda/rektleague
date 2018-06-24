# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0043_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='season_win',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
