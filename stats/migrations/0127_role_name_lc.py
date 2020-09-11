# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0126_role_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='name_lc',
            field=models.CharField(default=' ', max_length=15),
            preserve_default=False,
        ),
    ]
