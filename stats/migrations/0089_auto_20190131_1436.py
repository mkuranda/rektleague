# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0088_auto_20190131_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='youtube_link',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
