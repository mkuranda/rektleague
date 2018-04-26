# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0040_auto_20180425_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='regular',
            field=models.BooleanField(default=True),
        ),
    ]
