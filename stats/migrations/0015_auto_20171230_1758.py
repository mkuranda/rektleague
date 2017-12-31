# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0014_auto_20171230_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'stats/item/icon'),
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament_code',
            field=models.CharField(max_length=100),
        ),
    ]
