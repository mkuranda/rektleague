# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0031_series_splash'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='youtube_ext',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
