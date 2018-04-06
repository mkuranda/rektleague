# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0036_playermatch_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='HypeVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youtube_link', models.CharField(default=b'', max_length=100)),
                ('creator', models.ForeignKey(to='stats.Player')),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
    ]
