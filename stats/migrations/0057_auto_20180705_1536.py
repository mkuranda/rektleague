# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0056_seriesplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seriesplayer',
            name='series',
            field=models.ForeignKey(to='stats.Series'),
        ),
    ]
