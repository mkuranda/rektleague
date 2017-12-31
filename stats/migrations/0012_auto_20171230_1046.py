# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_team_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='icon',
            field=models.ImageField(upload_to=b'stats'),
        ),
    ]
