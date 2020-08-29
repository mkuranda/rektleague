# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0117_teaminvite_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='isPreseason',
            field=models.BooleanField(default=False),
        ),
    ]
