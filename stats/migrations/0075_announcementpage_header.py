# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0074_auto_20181220_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementpage',
            name='header',
            field=models.ImageField(default=b'', upload_to=b'stats/announcement_headers'),
        ),
    ]
