# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0119_auto_20200821_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='playoff_bracket',
            field=models.ImageField(default=b'', null=True, upload_to=b'stats/', blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='splash',
            field=models.ImageField(default=b'', null=True, upload_to=b'stats/season_splashes', blank=True),
        ),
    ]
