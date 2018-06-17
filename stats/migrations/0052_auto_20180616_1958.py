# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0051_auto_20180616_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='riot_subname',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='elitemonster',
            name='riot_subname',
            field=models.CharField(default=b'', max_length=25),
        ),
    ]
