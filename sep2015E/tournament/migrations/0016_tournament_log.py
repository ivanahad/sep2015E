# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0015_auto_20151206_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='log',
            field=models.TextField(blank=True, default=''),
        ),
    ]
