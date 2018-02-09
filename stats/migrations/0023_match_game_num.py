# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0022_auto_20180123_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='game_num',
            field=models.IntegerField(default=1),
        ),
    ]
