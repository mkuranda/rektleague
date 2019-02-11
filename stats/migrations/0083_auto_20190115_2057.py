# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0082_auto_20190115_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepagecarouselobject',
            old_name='url',
            new_name='url_name',
        ),
    ]
