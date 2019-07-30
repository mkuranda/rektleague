# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0097_teamplayertimeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamplayertimeline',
            name='gold_diff',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamplayertimeline',
            name='wards_killed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamplayertimeline',
            name='wards_placed',
            field=models.IntegerField(default=0),
        ),
    ]
