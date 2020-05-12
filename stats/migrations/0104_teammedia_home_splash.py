# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0103_player_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammedia',
            name='home_splash',
            field=models.ImageField(default=b'', upload_to=b'stats/team_splashes'),
        ),
    ]
