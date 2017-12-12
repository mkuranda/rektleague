# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20171210_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tournament_id', models.IntegerField(default=0)),
                ('team_size', models.IntegerField(default=5)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together=set([('team', 'role'), ('team', 'player')]),
        ),
        migrations.AddField(
            model_name='team',
            name='season',
            field=models.ForeignKey(default=1, to='stats.Season'),
            preserve_default=False,
        ),
    ]
