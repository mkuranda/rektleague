# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0128_leaveteamnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveteamnotification',
            name='role',
        ),
    ]
