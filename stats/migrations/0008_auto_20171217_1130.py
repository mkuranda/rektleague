# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_remove_match_riot_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('season', models.ForeignKey(to='stats.Season')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='week',
            field=models.ForeignKey(default=1, to='stats.Week'),
            preserve_default=False,
        ),
    ]
