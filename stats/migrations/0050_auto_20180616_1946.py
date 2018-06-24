# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0049_auto_20180614_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='EliteMonster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Lane',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='playermatchbuildingkill',
            name='lane',
        ),
        migrations.AlterField(
            model_name='playermatchbuildingkill',
            name='building_type',
            field=models.ForeignKey(to='stats.Building'),
        ),
        migrations.AlterField(
            model_name='playermatchelitemonsterkill',
            name='monster_type',
            field=models.ForeignKey(to='stats.EliteMonster'),
        ),
        migrations.AlterField(
            model_name='playermatchwardkill',
            name='ward_type',
            field=models.ForeignKey(to='stats.Ward'),
        ),
        migrations.AlterField(
            model_name='playermatchwardplace',
            name='ward_type',
            field=models.ForeignKey(to='stats.Ward'),
        ),
        migrations.AddField(
            model_name='building',
            name='lane',
            field=models.ForeignKey(to='stats.Lane'),
        ),
    ]
