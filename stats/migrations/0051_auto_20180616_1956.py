# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0050_auto_20180616_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='riot_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='building',
            name='riot_subname',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='elitemonster',
            name='riot_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='elitemonster',
            name='riot_subname',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lane',
            name='riot_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ward',
            name='riot_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
