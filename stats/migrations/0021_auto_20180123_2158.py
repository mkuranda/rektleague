# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_summonerspell_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tournament_code',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
