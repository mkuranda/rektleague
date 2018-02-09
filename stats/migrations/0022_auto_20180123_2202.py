# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0021_auto_20180123_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tournament_code',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
