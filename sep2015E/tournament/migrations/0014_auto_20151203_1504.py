# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0013_auto_20151203_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soloparticipant',
            name='tournament',
            field=models.ForeignKey(null=True, to='tournament.Tournament'),
        ),
        migrations.AlterField(
            model_name='tournamentparticipant',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
    ]
