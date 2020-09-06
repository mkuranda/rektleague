# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stats', '0121_season_numsubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPhotoRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'stats/player_photos')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='playerphotorequest',
            name='player',
        ),
        migrations.RemoveField(
            model_name='seasonplayer',
            name='player',
        ),
        migrations.RemoveField(
            model_name='seasonplayerrole',
            name='player',
        ),
        migrations.RemoveField(
            model_name='teaminvite',
            name='player',
        ),
        migrations.AddField(
            model_name='seasonplayer',
            name='user',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seasonplayerrole',
            name='user',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teaminvite',
            name='user',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PlayerPhotoRequest',
        ),
    ]
