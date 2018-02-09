# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0026_matchcaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='icon',
            field=models.ImageField(default=b'', upload_to=b'stats/role/icon'),
        ),
    ]
