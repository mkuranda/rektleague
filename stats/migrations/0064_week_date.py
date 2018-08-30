# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0063_series_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
