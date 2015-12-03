# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentparticipant',
            name='tournament',
            field=models.ForeignKey(null=True, to='tournament.Tournament'),
        ),
    ]
