# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0112_auto_20200820_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teaminvite',
            name='user',
        ),
        migrations.AddField(
            model_name='teaminvite',
            name='player',
            field=models.ForeignKey(default=1, to='stats.Player'),
            preserve_default=False,
        ),
    ]
