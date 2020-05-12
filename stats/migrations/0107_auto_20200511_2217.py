# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0106_teammedia_blurb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammedia',
            name='blurb',
            field=models.CharField(default=b'', max_length=500),
        ),
    ]
