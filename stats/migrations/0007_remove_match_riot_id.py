# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0006_auto_20171213_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='riot_id',
        ),
    ]
