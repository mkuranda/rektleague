# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20171220_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='icon',
            field=models.CharField(default=b'', max_length=40),
        ),
    ]
