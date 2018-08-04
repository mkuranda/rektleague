# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0059_auto_20180804_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamplayer',
            name='role',
            field=models.ForeignKey(default=None, to='stats.Role', null=True),
        ),
    ]
