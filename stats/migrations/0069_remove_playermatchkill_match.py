# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0068_auto_20180830_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermatchkill',
            name='match',
        ),
    ]
