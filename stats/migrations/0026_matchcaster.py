# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0025_auto_20180124_0702'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchCaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('match', models.ForeignKey(to='stats.Match')),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
    ]
