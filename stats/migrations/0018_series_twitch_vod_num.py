# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0017_auto_20180111_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='twitch_vod_num',
            field=models.IntegerField(default=0),
        ),
    ]
