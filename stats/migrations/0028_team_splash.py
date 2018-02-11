# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0027_role_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='splash',
            field=models.ImageField(default=b'', upload_to=b'stats/team_splashes'),
        ),
    ]
