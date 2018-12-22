# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0078_homepagestaticcontent_homepagestaticimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagestaticimage',
            name='style',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
