# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0125_teaminviteresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='title',
            field=models.CharField(default=' ', max_length=15),
            preserve_default=False,
        ),
    ]
