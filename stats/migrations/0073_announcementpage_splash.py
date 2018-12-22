# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0072_auto_20181220_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementpage',
            name='splash',
            field=models.ImageField(default=b'', upload_to=b'stats/announcement_splashes'),
        ),
    ]
