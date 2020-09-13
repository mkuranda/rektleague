# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0113_auto_20200820_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='icon',
            field=models.ImageField(null=True, upload_to=b'stats', blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='splash',
            field=models.ImageField(null=True, upload_to=b'stats/team_splashes', blank=True),
        ),
    ]
