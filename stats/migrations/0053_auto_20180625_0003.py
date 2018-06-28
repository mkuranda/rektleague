# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0052_auto_20180616_1958'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together=set([]),
        ),
    ]
