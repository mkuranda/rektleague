# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0092_auto_20190321_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamTimeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minute', models.IntegerField()),
                ('kills', models.FloatField(default=0)),
                ('building_kills', models.FloatField(default=0)),
                ('wards_placed', models.FloatField(default=0)),
                ('wards_killed', models.FloatField(default=0)),
                ('enemy_kills', models.FloatField(default=0)),
                ('enemy_building_kills', models.FloatField(default=0)),
                ('enemy_wards_placed', models.FloatField(default=0)),
                ('enemy_wards_killed', models.FloatField(default=0)),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
    ]
