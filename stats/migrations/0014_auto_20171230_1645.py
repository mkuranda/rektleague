# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0013_champion_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='champion',
            name='image',
        ),
        migrations.AddField(
            model_name='champion',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'stats/champion/icon'),
        ),
    ]
