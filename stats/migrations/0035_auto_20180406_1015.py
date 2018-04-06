# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0034_auto_20180330_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonChampion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('champion', models.ForeignKey(to='stats.Champion')),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
        migrations.AddField(
            model_name='champion',
            name='seasons',
            field=models.ManyToManyField(to='stats.Season', through='stats.SeasonChampion'),
        ),
    ]
