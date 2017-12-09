# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20171209_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='role',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
