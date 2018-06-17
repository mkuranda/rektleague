# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0047_playermatch_participant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatchtimeline',
            name='totalGold',
            field=models.IntegerField(default=0),
        ),
    ]
