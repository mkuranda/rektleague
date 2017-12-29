# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20171217_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('series', models.ForeignKey(to='stats.Series')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='week',
        ),
        migrations.AddField(
            model_name='week',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='series',
            name='week',
            field=models.ForeignKey(to='stats.Week'),
        ),
        migrations.AddField(
            model_name='match',
            name='series',
            field=models.ForeignKey(default=1, to='stats.Series'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='teamseries',
            unique_together=set([('team', 'series')]),
        ),
    ]
