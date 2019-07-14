# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0091_auto_20190205_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatchkill',
            name='position_x',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playermatchkill',
            name='position_y',
            field=models.IntegerField(default=0),
        ),
    ]
