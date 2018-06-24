# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0044_auto_20180614_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatch',
            name='role',
            field=models.ForeignKey(default=0, to='stats.Role'),
        ),
    ]
