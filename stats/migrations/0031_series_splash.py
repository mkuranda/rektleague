# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0030_auto_20180307_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='splash',
            field=models.ImageField(default=b'', upload_to=b'stats/champion/matchup_splashes'),
        ),
    ]
