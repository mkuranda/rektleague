# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0060_auto_20180804_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='isFill',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teamplayer',
            name='role',
            field=models.ForeignKey(default=0, to='stats.Role'),
            preserve_default=False,
        ),
    ]
