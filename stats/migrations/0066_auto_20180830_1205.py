# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0065_season_splash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playermatchbuildingassist',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchbuildingkill',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchbuildingkill',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchelitemonsterkill',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchelitemonsterkill',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchitem',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchitem',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchtimeline',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchtimeline',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchwardkill',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchwardkill',
            name='player',
        ),
        migrations.RemoveField(
            model_name='playermatchwardplace',
            name='match',
        ),
        migrations.RemoveField(
            model_name='playermatchwardplace',
            name='player',
        ),
        migrations.AddField(
            model_name='playermatchbuildingassist',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchbuildingkill',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchelitemonsterkill',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchitem',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchtimeline',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchwardkill',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playermatchwardplace',
            name='playermatch',
            field=models.ForeignKey(default=1, to='stats.PlayerMatch'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playermatchkill',
            name='killer',
            field=models.ForeignKey(to='stats.PlayerMatch'),
        ),
        migrations.AlterField(
            model_name='playermatchkill',
            name='victim',
            field=models.ForeignKey(related_name='victim', to='stats.PlayerMatch'),
        ),
    ]
