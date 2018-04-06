# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0032_series_youtube_ext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='youtube_ext',
            new_name='youtube_link',
        ),
    ]
