# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0099_testobject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testobject',
            name='content',
        ),
        migrations.AddField(
            model_name='testobject',
            name='gameId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testobject',
            name='losingTeam',
            field=models.CharField(default='', max_length=3000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testobject',
            name='shortCode',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testobject',
            name='winningTeam',
            field=models.CharField(default='', max_length=3000),
            preserve_default=False,
        ),
    ]
