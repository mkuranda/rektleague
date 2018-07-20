# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0054_auto_20180625_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermatch',
            name='champion',
            field=models.ForeignKey(default=0, to='stats.Champion'),
        ),
    ]
