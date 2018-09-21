# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0067_auto_20180830_1207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playermatchassist',
            old_name='player',
            new_name='playermatch',
        ),
    ]
