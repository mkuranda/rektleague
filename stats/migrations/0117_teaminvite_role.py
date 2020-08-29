# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0116_season_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvite',
            name='role',
            field=models.ForeignKey(default=1, to='stats.Role'),
            preserve_default=False,
        ),
    ]
