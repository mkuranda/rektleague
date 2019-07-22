# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0093_teamtimeline'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonTimeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minute', models.IntegerField()),
                ('kills', models.FloatField(default=0)),
                ('building_kills', models.FloatField(default=0)),
                ('wards_placed', models.FloatField(default=0)),
                ('wards_killed', models.FloatField(default=0)),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
    ]
