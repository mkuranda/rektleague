# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0053_auto_20180625_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(to='stats.Role')),
                ('team', models.ForeignKey(to='stats.Team')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='teamrole',
            unique_together=set([('team', 'role')]),
        ),
    ]
