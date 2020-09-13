# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0115_auto_20200820_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
