# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0080_homepageschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageCarouselObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True, null=True, blank=True)),
                ('url', models.CharField(max_length=100)),
                ('splash', models.ImageField(null=True, upload_to=b'stats/carousel_images', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='homepagecarousel',
            name='position',
        ),
        migrations.AlterUniqueTogether(
            name='homepagecarouselarticlelink',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='homepagecarouselarticlelink',
            name='announcement',
        ),
        migrations.RemoveField(
            model_name='homepagecarouselarticlelink',
            name='position',
        ),
        migrations.AlterUniqueTogether(
            name='homepagecarouselposition',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='homepagecarouselposition',
            name='carousel',
        ),
        migrations.RemoveField(
            model_name='homepageschedule',
            name='position',
        ),
        migrations.RemoveField(
            model_name='homepageschedule',
            name='season',
        ),
        migrations.RemoveField(
            model_name='homepagestaticcontent',
            name='position',
        ),
        migrations.RemoveField(
            model_name='homepagestaticimage',
            name='position',
        ),
        migrations.DeleteModel(
            name='HomePageCarousel',
        ),
        migrations.DeleteModel(
            name='HomePageCarouselArticleLink',
        ),
        migrations.DeleteModel(
            name='HomePageCarouselPosition',
        ),
        migrations.DeleteModel(
            name='HomePagePosition',
        ),
        migrations.DeleteModel(
            name='HomePageSchedule',
        ),
        migrations.DeleteModel(
            name='HomePageStaticContent',
        ),
        migrations.DeleteModel(
            name='HomePageStaticImage',
        ),
    ]
