# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0109_auto_20200728_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('blurb', models.CharField(max_length=1000)),
                ('warning', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('photo', models.ImageField(default=b'', upload_to=b'stats/merch_photos')),
            ],
        ),
    ]
