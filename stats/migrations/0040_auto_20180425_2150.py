# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0039_auto_20180425_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
