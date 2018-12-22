# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0071_auto_20181220_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcementpage',
            name='content',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='announcementpage',
            name='synopsis',
            field=models.CharField(max_length=100),
        ),
    ]
