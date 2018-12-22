# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0075_announcementpage_header'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePageAnnouncementLink',
            new_name='HomePageCarouselAnnouncementLink',
        ),
        migrations.AlterField(
            model_name='announcementpage',
            name='content',
            field=models.FileField(null=True, upload_to=b'stats/articles', blank=True),
        ),
        migrations.AlterField(
            model_name='announcementpage',
            name='header',
            field=models.ImageField(default=b'', null=True, upload_to=b'stats/announcement_headers', blank=True),
        ),
        migrations.AlterField(
            model_name='announcementpage',
            name='splash',
            field=models.ImageField(default=b'', null=True, upload_to=b'stats/announcement_splashes', blank=True),
        ),
        migrations.AlterField(
            model_name='announcementpage',
            name='url_name',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='homepagecarouselannouncementlink',
            name='position',
            field=models.ForeignKey(to='stats.HomePageCarouselPosition'),
        ),
        migrations.AlterField(
            model_name='homepageposition',
            name='number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='homepagecarouselannouncementlink',
            unique_together=set([('position', 'announcement')]),
        ),
        migrations.AlterUniqueTogether(
            name='homepagecarouselposition',
            unique_together=set([('number', 'carousel')]),
        ),
    ]
