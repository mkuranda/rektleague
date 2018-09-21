# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0062_summoner'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
