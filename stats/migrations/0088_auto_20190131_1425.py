# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0087_auto_20190131_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videopage',
            name='team_tag',
        ),
        migrations.AddField(
            model_name='articlepage',
            name='youtube_link',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.DeleteModel(
            name='VideoPage',
        ),
    ]
