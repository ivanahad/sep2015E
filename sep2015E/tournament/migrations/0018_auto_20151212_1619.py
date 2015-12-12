# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0017_tournament_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(related_name='team1', to='players.Pair', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(related_name='team2', to='players.Pair', null=True, blank=True),
        ),
    ]
