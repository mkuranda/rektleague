# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0016_auto_20180109_0754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammatchban',
            options={'ordering': ['champion']},
        ),
    ]
