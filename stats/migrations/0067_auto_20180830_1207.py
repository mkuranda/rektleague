# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0066_auto_20180830_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermatchassist',
            name='player',
            field=models.ForeignKey(to='stats.PlayerMatch'),
        ),
    ]
