# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0086_videopage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopage',
            name='content',
            field=models.FileField(null=True, upload_to=b'stats/video_articles', blank=True),
        ),
    ]
