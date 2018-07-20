# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0055_auto_20180705_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('role', models.ForeignKey(to='stats.Role')),
                ('series', models.ForeignKey(to='stats.Match')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
    ]
