# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0096_auto_20190721_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamPlayerTimeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minute', models.IntegerField()),
                ('gold', models.IntegerField(default=0)),
                ('enemy_gold', models.IntegerField(default=0)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('role', models.ForeignKey(to='stats.Role')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
    ]
