# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0035_auto_20180406_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermatch',
            name='team',
            field=models.ForeignKey(default=0, to='stats.Team'),
            preserve_default=False,
        ),
    ]
