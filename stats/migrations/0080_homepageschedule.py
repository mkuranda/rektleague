# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0079_homepagestaticimage_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.ForeignKey(blank=True, to='stats.HomePagePosition', null=True)),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
    ]
