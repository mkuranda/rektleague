# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_auto_20171230_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='image',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
