# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0120_auto_20200901_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='numSubs',
            field=models.IntegerField(default=3),
        ),
    ]
