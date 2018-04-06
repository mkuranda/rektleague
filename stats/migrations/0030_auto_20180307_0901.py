# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0029_match_riot_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teamplayer',
            unique_together=set([('team', 'player')]),
        ),
    ]
