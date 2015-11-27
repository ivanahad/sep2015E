# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0006_auto_20151126_2258'),
        ('tournament', '0004_auto_20151127_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='leader',
            field=models.ForeignKey(null=True, to='players.User'),
        ),
    ]
