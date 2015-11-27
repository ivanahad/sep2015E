# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_auto_20151127_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentnode',
            name='match',
            field=models.ForeignKey(to='tournament.Match', null=True, blank=True),
        ),
    ]
