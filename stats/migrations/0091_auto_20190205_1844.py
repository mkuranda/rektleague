# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0090_auto_20190205_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='left_splash',
            field=models.ImageField(null=True, upload_to=b'stats/team_splashes', blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='right_splash',
            field=models.ImageField(null=True, upload_to=b'stats/team_splashes', blank=True),
        ),
    ]
