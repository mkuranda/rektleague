# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0041_week_regular'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='title',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
