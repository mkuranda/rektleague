# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0019_auto_20180111_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='summonerspell',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'stats/summoner-spell/icon'),
        ),
    ]
