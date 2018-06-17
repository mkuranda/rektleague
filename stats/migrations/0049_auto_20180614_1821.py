# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0048_playermatchtimeline_totalgold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermatchbuildingkill',
            name='building_type',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='playermatchbuildingkill',
            name='lane',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='playermatchelitemonsterkill',
            name='monster_type',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='playermatchtimeline',
            name='position_x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playermatchtimeline',
            name='position_y',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playermatchwardkill',
            name='ward_type',
            field=models.CharField(default=b'', max_length=25),
        ),
        migrations.AlterField(
            model_name='playermatchwardplace',
            name='ward_type',
            field=models.CharField(default=b'', max_length=25),
        ),
    ]
