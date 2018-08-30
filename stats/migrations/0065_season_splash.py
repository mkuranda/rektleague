# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0064_week_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='splash',
            field=models.ImageField(default=b'', upload_to=b'stats/season_splashes'),
        ),
    ]
