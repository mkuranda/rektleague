# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0033_auto_20180330_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='youtube_link',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
