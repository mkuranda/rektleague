# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0085_articlepage_team_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_name', models.CharField(unique=True, max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('synopsis', models.CharField(max_length=100)),
                ('youtube_link', models.CharField(default=b'', max_length=100)),
                ('content', models.FileField(null=True, upload_to=b'stats/articles', blank=True)),
                ('splash', models.ImageField(default=b'', null=True, upload_to=b'stats/announcement_splashes', blank=True)),
                ('header', models.ImageField(default=b'', null=True, upload_to=b'stats/announcement_headers', blank=True)),
                ('team_tag', models.ManyToManyField(to='stats.Team')),
            ],
        ),
    ]
