# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0095_auto_20190721_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamplayer',
            name='killParticipation',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='teamplayer',
            name='teamDamagePercent',
            field=models.FloatField(default=0),
        ),
    ]
