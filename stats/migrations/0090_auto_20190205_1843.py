# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0089_auto_20190131_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='splash',
            field=models.ImageField(null=True, upload_to=b'stats/champion/matchup_splashes', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='youtube_link',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
