# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0100_auto_20190729_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('icon', models.ImageField(upload_to=b'stats')),
                ('splash', models.ImageField(default=b'', upload_to=b'stats/team_splashes')),
                ('banner', models.ImageField(upload_to=b'stats/team_banners')),
                ('left_splash', models.ImageField(upload_to=b'stats/team_splashes')),
                ('right_splash', models.ImageField(upload_to=b'stats/team_splashes')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='banner',
            field=models.ImageField(null=True, upload_to=b'stats/team_banners', blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='media',
            field=models.ForeignKey(default=1, to='stats.TeamMedia'),
            preserve_default=False,
        ),
    ]
