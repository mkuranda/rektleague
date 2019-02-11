# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0081_auto_20190115_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagecarouselobject',
            name='url',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
