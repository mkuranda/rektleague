# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0077_auto_20181220_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageStaticContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.FileField(null=True, upload_to=b'stats/articles', blank=True)),
                ('position', models.ForeignKey(blank=True, to='stats.HomePagePosition', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageStaticImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'', null=True, upload_to=b'stats/announcement_splashes', blank=True)),
                ('position', models.ForeignKey(blank=True, to='stats.HomePagePosition', null=True)),
            ],
        ),
    ]
