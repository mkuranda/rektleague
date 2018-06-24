# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0046_auto_20180614_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatch',
            name='participant_id',
            field=models.IntegerField(default=0),
        ),
    ]
