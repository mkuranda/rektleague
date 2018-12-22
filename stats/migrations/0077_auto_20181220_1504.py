# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0076_auto_20181220_1454'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnnouncementPage',
            new_name='ArticlePage',
        ),
        migrations.RenameModel(
            old_name='HomePageCarouselAnnouncementLink',
            new_name='HomePageCarouselArticleLink',
        ),
    ]
