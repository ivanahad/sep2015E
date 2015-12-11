# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20151125_1249'),
        ('tournament', '0016_tournament_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='staff',
            field=models.ForeignKey(null=True, to='staff.Staff', blank=True),
        ),
    ]
