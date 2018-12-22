# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0070_player_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('synopsis', models.CharField(max_length=400)),
                ('content', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageAnnouncementLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('announcement', models.ForeignKey(to='stats.AnnouncementPage')),
            ],
        ),
        migrations.CreateModel(
            name='HomePageCarousel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageCarouselPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('carousel', models.ForeignKey(to='stats.HomePageCarousel')),
            ],
        ),
        migrations.CreateModel(
            name='HomePagePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SeriesCastPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='stats.Player')),
                ('role', models.ForeignKey(to='stats.Role')),
                ('series', models.ForeignKey(to='stats.Series')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesCastTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('series', models.ForeignKey(to='stats.Series')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.AddField(
            model_name='homepagecarousel',
            name='position',
            field=models.ForeignKey(blank=True, to='stats.HomePagePosition', null=True),
        ),
        migrations.AddField(
            model_name='homepageannouncementlink',
            name='position',
            field=models.ForeignKey(to='stats.HomePagePosition'),
        ),
    ]
