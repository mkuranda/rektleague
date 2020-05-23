# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0107_auto_20200511_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='playoff_bracket',
            field=models.ImageField(default=b'', upload_to=b'stats/'),
        ),
    ]
