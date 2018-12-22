# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0073_announcementpage_splash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcementpage',
            name='content',
            field=models.FileField(upload_to=b'stats/articles'),
        ),
    ]
